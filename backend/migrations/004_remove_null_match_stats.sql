-- Delete any match_stats rows with null or empty user_id
BEGIN;

-- The `user_id` column is an INTEGER; comparing it to an empty string causes a type error.
-- Only delete rows where `user_id IS NULL`.
DELETE FROM match_stats WHERE user_id IS NULL;

COMMIT;