-- Migration: Remove match_stats trigger to avoid double-counting
-- The application now manages detailed per-player stats; the DB trigger
-- previously incremented `total_matches` as well, causing duplicate counts.

BEGIN;

-- Drop the trigger that auto-updated match_stats on matches updates
DROP TRIGGER IF EXISTS match_completion_trigger ON matches;

-- Remove the old trigger function
DROP FUNCTION IF EXISTS update_match_stats();

COMMIT;
