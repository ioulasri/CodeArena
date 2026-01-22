-- ============================================================
-- Table: users
-- Description: Stores user account information and profiles
-- ============================================================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    bio TEXT,
    avatar_url VARCHAR(255)
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);

-- ============================================================
-- Table: problems
-- Description: Stores coding problems and their metadata
-- ============================================================
CREATE TABLE problems (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    difficulty VARCHAR(20) NOT NULL, -- EASY, MEDIUM, HARD
    category VARCHAR(50),
    tags JSONB,
    time_limit_ms INTEGER DEFAULT 1000,
    memory_limit_mb INTEGER DEFAULT 256,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by_id INTEGER REFERENCES users(id)
);

CREATE INDEX idx_problems_difficulty ON problems(difficulty);
CREATE INDEX idx_problems_category ON problems(category);
CREATE INDEX idx_problems_created_at ON problems(created_at);

-- ============================================================
-- Table: test_cases
-- Description: Stores test cases for problem validation
-- ============================================================
CREATE TABLE test_cases (
    id SERIAL PRIMARY KEY,
    problem_id INTEGER NOT NULL REFERENCES problems(id) ON DELETE CASCADE,
    input_data TEXT NOT NULL,
    expected_output TEXT NOT NULL,
    is_sample BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_test_cases_problem_id ON test_cases(problem_id);

-- ============================================================
-- Table: submissions
-- Description: Stores user code submissions and execution results
-- ============================================================
CREATE TABLE submissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    problem_id INTEGER NOT NULL REFERENCES problems(id),
    code TEXT NOT NULL,
    language VARCHAR(20) NOT NULL, -- python, javascript, java, cpp
    status VARCHAR(20) NOT NULL, -- PENDING, ACCEPTED, WRONG_ANSWER, TIME_LIMIT_EXCEEDED, RUNTIME_ERROR
    execution_time_ms FLOAT,
    memory_used_mb FLOAT,
    test_cases_passed INTEGER,
    test_cases_total INTEGER,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_submissions_user_id ON submissions(user_id);
CREATE INDEX idx_submissions_problem_id ON submissions(problem_id);
CREATE INDEX idx_submissions_created_at ON submissions(created_at);
CREATE INDEX idx_submissions_status ON submissions(status);

-- ============================================================
-- Table: leaderboard
-- Description: Tracks user rankings and problem-solving statistics
-- ============================================================
CREATE TABLE leaderboard (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES users(id),
    problems_solved INTEGER DEFAULT 0,
    total_points INTEGER DEFAULT 0,
    ranking INTEGER,
    last_submission_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_leaderboard_ranking ON leaderboard(ranking);
CREATE INDEX idx_leaderboard_updated_at ON leaderboard(updated_at);

-- ============================================================
-- Table: contests
-- Description: Stores competitive programming contest information
-- ============================================================
CREATE TABLE contests (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    status VARCHAR(20), -- UPCOMING, ONGOING, COMPLETED
    created_by_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_contests_start_time ON contests(start_time);
CREATE INDEX idx_contests_status ON contests(status);
