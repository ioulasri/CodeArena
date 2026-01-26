-- Migration: Seed sample puzzles for testing/demo
BEGIN;

INSERT INTO puzzles (day, title, description, story, difficulty, generator_type, generator_params)
VALUES
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
 '{"height": 15, "max_value": 50}'::jsonb)
ON CONFLICT (day) DO UPDATE SET
    title = EXCLUDED.title,
    description = EXCLUDED.description,
    story = EXCLUDED.story,
    difficulty = EXCLUDED.difficulty,
    generator_type = EXCLUDED.generator_type,
    generator_params = EXCLUDED.generator_params;

COMMIT;
