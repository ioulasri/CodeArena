-- Migration: Add performance indexes
-- Description: Add indexes on frequently queried columns for better performance

-- Index on matches.status for filtering waiting/active matches
CREATE INDEX IF NOT EXISTS idx_matches_status ON matches(status);

-- Index on matches.puzzle_id for joining with puzzles
CREATE INDEX IF NOT EXISTS idx_matches_puzzle_id ON matches(puzzle_id);

-- Index on matches.player1_id for user match queries
CREATE INDEX IF NOT EXISTS idx_matches_player1_id ON matches(player1_id);

-- Index on matches.player2_id for user match queries
CREATE INDEX IF NOT EXISTS idx_matches_player2_id ON matches(player2_id);

-- Index on matches.winner_id for leaderboard queries
CREATE INDEX IF NOT EXISTS idx_matches_winner_id ON matches(winner_id);

-- Composite index for finding waiting public matches
CREATE INDEX IF NOT EXISTS idx_matches_waiting_public 
ON matches(puzzle_id, status, room_code, player2_id) 
WHERE status = 'waiting' AND room_code IS NULL AND player2_id IS NULL;

-- Index on player_answers.match_id for answer lookups
CREATE INDEX IF NOT EXISTS idx_player_answers_match_id ON player_answers(match_id);

-- Index on player_answers.player_id for user answer history
CREATE INDEX IF NOT EXISTS idx_player_answers_player_id ON player_answers(player_id);

-- Composite index for correct answers
CREATE INDEX IF NOT EXISTS idx_player_answers_correct 
ON player_answers(match_id, player_id, is_correct) 
WHERE is_correct = true;

-- Index on player_puzzle_inputs.match_id for input lookups
CREATE INDEX IF NOT EXISTS idx_player_puzzle_inputs_match_id ON player_puzzle_inputs(match_id);

-- Index on player_puzzle_inputs.player_id for user inputs
CREATE INDEX IF NOT EXISTS idx_player_puzzle_inputs_player_id ON player_puzzle_inputs(player_id);

-- Composite index for player-specific puzzle inputs
CREATE INDEX IF NOT EXISTS idx_player_puzzle_inputs_match_player 
ON player_puzzle_inputs(match_id, player_id);

-- Index on match_stats.user_id (already unique, but explicit index)
CREATE INDEX IF NOT EXISTS idx_match_stats_user_id ON match_stats(user_id);

-- Index on puzzles.is_active for filtering active puzzles
CREATE INDEX IF NOT EXISTS idx_puzzles_is_active ON puzzles(is_active);

-- Index on puzzles.day for ordering
CREATE INDEX IF NOT EXISTS idx_puzzles_day ON puzzles(day);
