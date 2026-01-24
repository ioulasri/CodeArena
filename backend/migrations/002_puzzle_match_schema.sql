-- Migration: Convert from LeetCode-style to Puzzle Match System
-- This supports Advent of Code style competitive puzzle solving

-- Drop old tables (if you want to keep old data, comment these out)
-- DROP TABLE IF EXISTS submissions CASCADE;
-- DROP TABLE IF EXISTS problems CASCADE;
-- DROP TABLE IF EXISTS contests CASCADE;

-- Puzzles Table - Stores puzzle definitions
CREATE TABLE IF NOT EXISTS puzzles (
    id SERIAL PRIMARY KEY,
    day INTEGER NOT NULL UNIQUE,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    story TEXT, -- Fun narrative/story for the puzzle
    difficulty VARCHAR(20) DEFAULT 'medium', -- easy, medium, hard
    generator_type VARCHAR(50) NOT NULL, -- Type of puzzle generator to use
    generator_params JSONB DEFAULT '{}', -- Parameters for puzzle generation
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Matches Table - Stores game matches between players
CREATE TABLE IF NOT EXISTS matches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    puzzle_id INTEGER REFERENCES puzzles(id) ON DELETE CASCADE,
    player1_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    player2_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'waiting', -- waiting, ready, active, completed, abandoned
    winner_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    room_code VARCHAR(10) UNIQUE, -- Optional room code for private matches
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT different_players CHECK (player1_id != player2_id)
);

-- Player Puzzle Inputs - Unique inputs for each player in a match
CREATE TABLE IF NOT EXISTS player_puzzle_inputs (
    id SERIAL PRIMARY KEY,
    match_id UUID REFERENCES matches(id) ON DELETE CASCADE,
    player_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    puzzle_id INTEGER REFERENCES puzzles(id) ON DELETE CASCADE,
    input_data TEXT NOT NULL, -- The unique puzzle input for this player
    expected_answer TEXT NOT NULL, -- The correct answer for this input
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(match_id, player_id)
);

-- Player Answers - Track answer submissions
CREATE TABLE IF NOT EXISTS player_answers (
    id SERIAL PRIMARY KEY,
    match_id UUID REFERENCES matches(id) ON DELETE CASCADE,
    player_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    puzzle_id INTEGER REFERENCES puzzles(id) ON DELETE CASCADE,
    submitted_answer TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_taken_seconds INTEGER -- Time from match start to submission
);

-- Match Stats - Aggregate statistics
CREATE TABLE IF NOT EXISTS match_stats (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE UNIQUE,
    total_matches INTEGER DEFAULT 0,
    matches_won INTEGER DEFAULT 0,
    matches_lost INTEGER DEFAULT 0,
    total_puzzles_solved INTEGER DEFAULT 0,
    fastest_solve_seconds INTEGER,
    average_solve_seconds FLOAT,
    current_streak INTEGER DEFAULT 0,
    best_streak INTEGER DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Leaderboard View
CREATE OR REPLACE VIEW leaderboard AS
SELECT 
    u.id,
    u.username,
    ms.total_matches,
    ms.matches_won,
    ms.matches_lost,
    CASE 
        WHEN ms.total_matches > 0 THEN ROUND((ms.matches_won::float / ms.total_matches::float * 100)::numeric, 2)
        ELSE 0 
    END as win_rate,
    ms.total_puzzles_solved,
    ms.fastest_solve_seconds,
    ms.average_solve_seconds,
    ms.current_streak,
    ms.best_streak
FROM users u
LEFT JOIN match_stats ms ON u.id = ms.user_id
ORDER BY ms.matches_won DESC, ms.average_solve_seconds ASC;

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_matches_status ON matches(status);
CREATE INDEX IF NOT EXISTS idx_matches_players ON matches(player1_id, player2_id);
CREATE INDEX IF NOT EXISTS idx_matches_puzzle ON matches(puzzle_id);
CREATE INDEX IF NOT EXISTS idx_matches_room_code ON matches(room_code);
CREATE INDEX IF NOT EXISTS idx_player_answers_match ON player_answers(match_id);
CREATE INDEX IF NOT EXISTS idx_player_puzzle_inputs_match ON player_puzzle_inputs(match_id);

-- Function to update match stats after a match completes
CREATE OR REPLACE FUNCTION update_match_stats()
RETURNS TRIGGER AS $$
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
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER match_completion_trigger
AFTER UPDATE ON matches
FOR EACH ROW
EXECUTE FUNCTION update_match_stats();

-- Insert sample puzzles
INSERT INTO puzzles (day, title, description, story, difficulty, generator_type, generator_params) VALUES
(1, 'The Crystal Cave Numbers', 
 'You discover a cave filled with mysterious crystals. Each crystal has a number etched on it. Your task is to find the sum of all crystals whose numbers are multiples of 3 or 5.',
 'Deep in the mountains, ancient crystals hold mathematical secrets. Only those who can decode them quickly will claim victory!',
 'easy',
 'crystal_sum',
 '{"min_count": 50, "max_count": 100, "range": 1000}'::jsonb),

(2, 'The Encrypted Scroll',
 'An ancient scroll contains a sequence of characters. Count how many times the word pattern appears in the text, including overlapping occurrences.',
 'The scroll''s secrets are hidden in plain sight. Speed and accuracy will determine who unlocks its mysteries first!',
 'medium',
 'pattern_counter',
 '{"text_length": 500, "pattern_length": 5}'::jsonb),

(3, 'The Magic Grid',
 'You find a grid of numbers. Starting from the top-left, you can only move right or down. Find the path with the maximum sum.',
 'The magic grid shifts for each challenger. Navigate wisely to maximize your treasure!',
 'medium',
 'grid_path',
 '{"rows": 10, "cols": 10, "max_value": 100}'::jsonb),

(4, 'The Sequence Cipher',
 'A sequence of numbers follows a hidden pattern. Find the next 3 numbers in the sequence.',
 'Ancient mathematicians left this cipher as a test. Can you decode it faster than your opponent?',
 'hard',
 'sequence_finder',
 '{"sequence_length": 8, "difficulty": "medium"}'::jsonb),

(5, 'The Tower of Blocks',
 'Blocks are stacked in a tower. Each block has a value. Find the maximum value you can get by removing blocks, but you can only remove a block if all blocks above it have been removed.',
 'The Tower of Blocks challenges your strategic thinking. Choose wisely, choose quickly!',
 'hard',
 'tower_blocks',
 '{"height": 15, "max_value": 50}'::jsonb);
