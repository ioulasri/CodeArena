-- Migration: Recompute and fix match_stats from raw matches and player_answers
-- This will recompute aggregates for all users and update the trigger to maintain puzzle stats

BEGIN;

-- Recompute aggregates and upsert into match_stats
INSERT INTO match_stats (user_id, total_matches, matches_won, matches_lost, total_puzzles_solved, fastest_solve_seconds, average_solve_seconds, current_streak, best_streak, updated_at)
SELECT
  u.id AS user_id,
  COALESCE((SELECT COUNT(*) FROM matches m WHERE (m.player1_id = u.id OR m.player2_id = u.id) AND m.status = 'completed'), 0) AS total_matches,
  COALESCE((SELECT COUNT(*) FROM matches m WHERE m.winner_id = u.id AND m.status = 'completed'), 0) AS matches_won,
  COALESCE((SELECT COUNT(*) FROM matches m WHERE (m.player1_id = u.id OR m.player2_id = u.id) AND m.status = 'completed' AND m.winner_id IS NOT NULL AND m.winner_id != u.id), 0) AS matches_lost,
  COALESCE((SELECT COUNT(*) FROM player_answers pa WHERE pa.player_id = u.id AND pa.is_correct = true), 0) AS total_puzzles_solved,
  -- If user has no completed matches or no correct answers, normalize to 0
  CASE WHEN COALESCE((SELECT COUNT(*) FROM matches m WHERE (m.player1_id = u.id OR m.player2_id = u.id) AND m.status = 'completed'),0) = 0 THEN 0
      ELSE COALESCE((SELECT MIN(pa.time_taken_seconds) FROM player_answers pa WHERE pa.player_id = u.id AND pa.is_correct = true), 0)
  END AS fastest_solve_seconds,
  CASE WHEN COALESCE((SELECT COUNT(*) FROM matches m WHERE (m.player1_id = u.id OR m.player2_id = u.id) AND m.status = 'completed'),0) = 0 THEN 0
      ELSE COALESCE(ROUND((SELECT AVG(pa.time_taken_seconds) FROM player_answers pa WHERE pa.player_id = u.id AND pa.is_correct = true)::numeric,2), 0)
  END AS average_solve_seconds,
  0 AS current_streak,
  0 AS best_streak,
  CURRENT_TIMESTAMP AS updated_at
FROM users u
ON CONFLICT (user_id) DO UPDATE SET
  total_matches = EXCLUDED.total_matches,
  matches_won = EXCLUDED.matches_won,
  matches_lost = EXCLUDED.matches_lost,
  total_puzzles_solved = EXCLUDED.total_puzzles_solved,
  fastest_solve_seconds = EXCLUDED.fastest_solve_seconds,
  average_solve_seconds = EXCLUDED.average_solve_seconds,
  updated_at = EXCLUDED.updated_at;

-- Replace update_match_stats() to also recompute puzzle aggregates for the two players involved
CREATE OR REPLACE FUNCTION update_match_stats()
RETURNS TRIGGER AS $$
DECLARE
  p_id INTEGER;
  total_solved INTEGER;
  fastest INTEGER;
  avg_time DOUBLE PRECISION;
BEGIN
    IF NEW.status = 'completed' AND OLD.status != 'completed' THEN
        -- Update stats for both players
        INSERT INTO match_stats (user_id, total_matches)
        VALUES (NEW.player1_id, 1), (NEW.player2_id, 1)
        ON CONFLICT (user_id)
        DO UPDATE SET
            total_matches = match_stats.total_matches + 1,
            updated_at = CURRENT_TIMESTAMP;
        
        -- Update winner stats
        IF NEW.winner_id IS NOT NULL THEN
            UPDATE match_stats 
            SET 
                matches_won = matches_won + 1,
                current_streak = current_streak + 1,
                best_streak = GREATEST(best_streak, current_streak + 1),
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = NEW.winner_id;
            
            -- Update loser stats (reset streak)
            UPDATE match_stats
            SET 
                matches_lost = matches_lost + 1,
                current_streak = 0,
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id IN (NEW.player1_id, NEW.player2_id) 
            AND user_id != NEW.winner_id;
        END IF;

        -- Recompute puzzle aggregates (total_solved, fastest, average) for both players from player_answers
        FOR p_id IN SELECT DISTINCT unnest(array[NEW.player1_id, NEW.player2_id]) LOOP
            SELECT COUNT(*) INTO total_solved FROM player_answers pa WHERE pa.player_id = p_id AND pa.is_correct = true;
            SELECT MIN(pa.time_taken_seconds) INTO fastest FROM player_answers pa WHERE pa.player_id = p_id AND pa.is_correct = true;
            SELECT AVG(pa.time_taken_seconds) INTO avg_time FROM player_answers pa WHERE pa.player_id = p_id AND pa.is_correct = true;

            -- Ensure a match_stats row exists
            INSERT INTO match_stats (user_id, total_matches, total_puzzles_solved, fastest_solve_seconds, average_solve_seconds, updated_at)
            VALUES (p_id, COALESCE((SELECT total_matches FROM match_stats WHERE user_id = p_id), 0), COALESCE(total_solved, 0), COALESCE(fastest, 0), COALESCE(ROUND(avg_time::numeric,2), 0), CURRENT_TIMESTAMP)
            ON CONFLICT (user_id) DO UPDATE SET
                total_puzzles_solved = COALESCE(EXCLUDED.total_puzzles_solved, match_stats.total_puzzles_solved),
                fastest_solve_seconds = COALESCE(EXCLUDED.fastest_solve_seconds, match_stats.fastest_solve_seconds),
                average_solve_seconds = COALESCE(EXCLUDED.average_solve_seconds, match_stats.average_solve_seconds),
                updated_at = CURRENT_TIMESTAMP;
        END LOOP;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

COMMIT;
