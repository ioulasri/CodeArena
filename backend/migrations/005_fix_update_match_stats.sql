-- Migration: Fix update_match_stats to avoid inserting NULL user_id rows
BEGIN;

CREATE OR REPLACE FUNCTION update_match_stats()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'completed' AND OLD.status != 'completed' THEN
        -- Insert or increment total_matches for non-null players only
        INSERT INTO match_stats (user_id, total_matches)
        SELECT p_id, 1
        FROM (VALUES (NEW.player1_id), (NEW.player2_id)) AS t(p_id)
        WHERE p_id IS NOT NULL
        ON CONFLICT (user_id) DO UPDATE SET
            total_matches = match_stats.total_matches + 1,
            updated_at = CURRENT_TIMESTAMP;

        -- Update winner stats if present
        IF NEW.winner_id IS NOT NULL THEN
            UPDATE match_stats
            SET
                matches_won = COALESCE(matches_won,0) + 1,
                current_streak = COALESCE(current_streak,0) + 1,
                best_streak = GREATEST(COALESCE(best_streak,0), COALESCE(current_streak,0) + 1),
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = NEW.winner_id;

            -- Update loser stats (reset streak) for the other participant(s)
            UPDATE match_stats
            SET
                matches_lost = COALESCE(matches_lost,0) + 1,
                current_streak = 0,
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id IN (
                SELECT p_id FROM (VALUES (NEW.player1_id),(NEW.player2_id)) AS t(p_id)
                WHERE p_id IS NOT NULL
            ) AND user_id != NEW.winner_id;
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

COMMIT;
