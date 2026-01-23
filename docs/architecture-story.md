# 🏛️ CodeArena Architecture: The Story So Far

> *A journey through your competitive programming platform*

---

## 📖 Chapter 1: The Foundation (What You Built)

### The Beginning: A User Arrives

Imagine a developer named Alex visiting CodeArena for the first time. Let's follow their journey and see how your backend handles each step:

```
Alex → Frontend → Backend API → Database → Response
```

### Act 1: Registration & Authentication

**Alex visits your site and clicks "Sign Up"**

1. **The Request Journey**
   ```
   POST /api/v1/auth/register
   Body: { username: "alex", email: "alex@dev.com", password: "secret123" }
   ```

2. **What Happens Inside** (`backend/app/api/v1/endpoints/auth.py`)
   - The request hits your **auth endpoint**
   - FastAPI validates the data using **Pydantic schemas** (`UserCreate`)
   - The endpoint calls `hash_password()` from `core/security.py`
   - **Bcrypt** transforms "secret123" into gibberish: `$2b$12$xyz...`
   - A new **User** is created in the database (SQLAlchemy model)
   - PostgreSQL stores it in the `users` table
   - Response: Alex's user profile (without the password!)

3. **The Security Layer**
   - Passwords are NEVER stored in plain text
   - Bcrypt hashing is one-way (can't reverse it)
   - Even if hackers steal the database, passwords are safe

### Act 2: Login & The Magic Token

**Alex comes back the next day and logs in**

1. **The Login Flow**
   ```
   POST /api/v1/auth/login
   Body: { username: "alex", password: "secret123" }
   ```

2. **Authentication Magic** (`core/security.py`)
   - Your code finds Alex's user record
   - Checks if `verify_password("secret123", stored_hash)` → True ✅
   - Creates a **JWT token** (like a temporary ID card)
   - Token contains: `{ sub: "alex", exp: "2026-01-24 03:00:00" }`
   - Signed with your SECRET_KEY (so it can't be forged)

3. **The Token**
   ```json
   {
     "access_token": "eyJhbGc...xyz",
     "token_type": "bearer"
   }
   ```
   - This is Alex's **passport** for the next 30 days
   - Frontend stores it (localStorage or cookie)
   - Sends it with every request: `Authorization: Bearer eyJhbGc...xyz`

### Act 3: Protected Routes

**Alex wants to see their profile**

1. **The Guarded Door**
   ```
   GET /api/v1/auth/me
   Headers: Authorization: Bearer eyJhbGc...xyz
   ```

2. **The Bouncer** (`get_current_user_dependency`)
   - Extracts the token from the Authorization header
   - Decodes it using SECRET_KEY
   - Validates it's not expired
   - Looks up "alex" in the database
   - Returns the User object to the endpoint

3. **Access Granted**
   - Endpoint gets the authenticated User
   - Returns Alex's profile data
   - No password in response (security!)

---

## 🏗️ Chapter 2: The Database Architecture

### The Data Model (Your Tables)

Think of your database as a **library with 6 special shelves**:

#### 1. **Users Shelf** (`users` table)
```
📚 User Record
├─ id: 1
├─ username: "alex"
├─ email: "alex@dev.com"
├─ password_hash: "$2b$12$xyz..." (encrypted!)
├─ is_active: true
├─ bio: "Love Python"
├─ avatar_url: "https://..."
├─ created_at: "2026-01-22 03:12:38"
└─ updated_at: "2026-01-22 03:12:38"
```

#### 2. **Problems Shelf** (`problems` table)
```
📚 Problem Record
├─ id: 1
├─ title: "Two Sum"
├─ slug: "two-sum" (for URLs)
├─ description: "Given an array of integers..."
├─ difficulty: "EASY"
├─ category: "Arrays"
├─ tags: ["array", "hash-table"] (JSONB - flexible!)
├─ constraints: "1 <= nums.length <= 10^4"
├─ examples: [ { input: "[2,7]", output: "[0,1]" } ]
├─ time_limit_ms: 2000
├─ memory_limit_mb: 128
├─ acceptance_rate: 45.5
├─ is_premium: false
└─ created_at: "2026-01-22"
```

#### 3. **Test Cases Shelf** (`test_cases` table)
```
📚 Test Case Record (CURRENTLY NOT USED - more on this later!)
├─ id: 1
├─ problem_id: 1 (belongs to "Two Sum")
├─ input_data: "[2,7,11,15]\n9"
├─ expected_output: "[0,1]"
├─ is_sample: true (visible to users)
└─ points: 10
```

#### 4. **Submissions Shelf** (`submissions` table)
```
📚 Submission Record
├─ id: 1
├─ problem_id: 1
├─ user_id: 1 (Alex's submission)
├─ code: "def solution(nums, target): ..."
├─ language: "python"
├─ status: "PENDING" ⏳ (or ACCEPTED ✅, WRONG_ANSWER ❌, ERROR 💥)
├─ execution_time_ms: null (will be filled after execution)
├─ memory_used_mb: null
├─ test_cases_passed: null (will be filled)
├─ test_cases_total: null
├─ error_message: null
└─ created_at: "2026-01-23"
```

#### 5. **Leaderboard Shelf** (`leaderboard` table)
```
📚 Leaderboard Entry
├─ id: 1
├─ user_id: 1
├─ problems_solved: 0 (will increase)
├─ total_submissions: 0
├─ acceptance_rate: 0.0
├─ total_score: 0
└─ rank: 999
```

#### 6. **Contests Shelf** (`contests` table)
```
📚 Contest Record
├─ id: 1
├─ title: "Weekly Contest 385"
├─ description: "4 problems, 90 minutes"
├─ start_time: "2026-01-25 14:00:00"
├─ end_time: "2026-01-25 15:30:00"
├─ status: "UPCOMING"
└─ created_by_id: 1 (Alex created it)
```

### The Relationships (How Tables Connect)

```
Users ─────┐
           ├──→ Submissions ←─── Problems ←─── Test Cases
           └──→ Contests
                    ↓
              Leaderboard
```

- **Users create Submissions** for **Problems**
- **Problems have Test Cases**
- **Users compete in Contests**
- **Leaderboard tracks Users' scores**

---

## 🎭 Chapter 3: The Current State

### What Works Right Now ✅

1. **Authentication System** - Complete and tested
   - Register new users
   - Login and get JWT tokens
   - Protected routes with token validation

2. **User Management**
   - List all users
   - Get user by ID or username
   - View user profiles

3. **Problem Browsing**
   - List problems (with filters by difficulty/category)
   - Get problem details by ID or slug
   - Create new problems

4. **Submission Recording**
   - Users can submit code
   - Submissions are stored in database
   - Can view submission history

5. **Database & Infrastructure**
   - PostgreSQL running in Docker
   - FastAPI backend running in Docker
   - Health checks working
   - Swagger docs at `/docs`

### The Big Missing Piece 🚨

**Alex submits code...**

```python
# Alex's solution to "Two Sum"
def solution(nums, target):
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
```

**What happens now:**
1. ✅ Code is saved to database
2. ✅ Status set to "PENDING"
3. ❌ **NOTHING ELSE!**

**What SHOULD happen:**
1. Code is saved
2. **Code is executed in a secure sandbox**
3. **Tested against all test cases**
4. **Results calculated** (execution time, memory, pass/fail)
5. **Status updated** (ACCEPTED, WRONG_ANSWER, TIME_LIMIT_EXCEEDED, etc.)
6. **Leaderboard updated** if accepted
7. **User gets instant feedback**

---

## 🔮 Chapter 4: The Missing Magic (What's Next)

### The Code Execution Engine - The Heart of CodeArena

This is what separates a "form that saves code" from a "competitive programming platform."

#### The Journey of a Submission

```
┌─────────────────────────────────────────────────────────────────┐
│  1. USER SUBMITS CODE                                           │
│     POST /api/v1/submissions/                                   │
│     { problem_id: 1, code: "...", language: "python" }         │
└────────────────────────┬────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│  2. SAVE TO DATABASE                                            │
│     status = "PENDING"                                          │
│     submission_id = 123                                         │
└────────────────────────┬────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│  3. QUEUE FOR EXECUTION (New! To be built)                     │
│     Add to Celery task queue or background task                 │
│     Return submission_id to user immediately                    │
└────────────────────────┬────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│  4. CODE EXECUTION WORKER (New! To be built)                   │
│     - Fetch test cases from database                            │
│     - For each test case:                                       │
│       a. Create isolated Docker container                       │
│       b. Copy user code into container                          │
│       c. Run code with test input                               │
│       d. Capture output, time, memory                           │
│       e. Compare output with expected                           │
│       f. Kill container after timeout                           │
└────────────────────────┬────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│  5. UPDATE DATABASE                                             │
│     status = "ACCEPTED" (or WRONG_ANSWER, etc.)                │
│     test_cases_passed = 8/10                                    │
│     execution_time_ms = 45.2                                    │
│     memory_used_mb = 12.4                                       │
└────────────────────────┬────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│  6. UPDATE LEADERBOARD (New! To be built)                      │
│     If ACCEPTED:                                                │
│       - Increment problems_solved                               │
│       - Add points to total_score                               │
│       - Recalculate rank                                        │
└────────────────────────┬────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│  7. NOTIFY USER (Future enhancement)                            │
│     WebSocket push notification                                 │
│     "Your submission has been judged: ACCEPTED! 🎉"            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Chapter 5: Your Next Steps (The Roadmap)

### Phase 1: Make Submissions Actually Work (Week 2)

#### Step 1.1: Create Test Cases for Problems
**File to create:** `backend/scripts/seed_data.py`

Add sample problems with test cases to your database:
```python
# Two Sum problem with 5 test cases
problem = Problem(
    title="Two Sum",
    slug="two-sum",
    difficulty="EASY",
    # ... other fields
)
test_cases = [
    TestCase(problem_id=1, input="[2,7,11,15]\n9", expected="[0,1]"),
    TestCase(problem_id=1, input="[3,2,4]\n6", expected="[1,2]"),
    # ... more test cases
]
```

#### Step 1.2: Build the Code Executor
**File to create:** `backend/app/services/code_executor.py`

This service will:
- Take code + test cases
- Run code in Docker container
- Return results (pass/fail, time, memory)

```python
class CodeExecutor:
    async def execute(self, code: str, language: str, test_case: TestCase):
        # Create temp directory
        # Write code to file
        # Run in Docker: docker run --rm -v ... python:3.11 python solution.py
        # Capture output and metrics
        # Clean up
        return ExecutionResult(...)
```

#### Step 1.3: Build the Submission Evaluator
**File to create:** `backend/app/services/submission_evaluator.py`

This orchestrates the whole judging process:
```python
class SubmissionEvaluator:
    async def evaluate(self, submission_id: int):
        # Get submission from DB
        # Get problem's test cases
        # Run code_executor for each test case
        # Calculate final verdict
        # Update submission status in DB
        # Update leaderboard
```

#### Step 1.4: Connect to Submission Endpoint
**File to modify:** `backend/app/api/v1/endpoints/submissions.py`

```python
@router.post("/", response_model=SubmissionResponse)
async def create_submission(
    submission_data: SubmissionCreate,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks  # New!
):
    # Save submission (status=PENDING)
    db.add(db_submission)
    db.commit()
    
    # Queue for evaluation (runs asynchronously)
    background_tasks.add_task(
        evaluate_submission,
        submission_id=db_submission.id
    )
    
    return db_submission  # Returns immediately while evaluation runs
```

### Phase 2: Polish & Enhance (Week 3)

1. **Admin System**
   - Add `is_admin` field to User model
   - Create admin middleware
   - Protect problem creation endpoint

2. **Contest System**
   - Create contest endpoints (CRUD)
   - Contest start/end logic
   - Contest-specific leaderboard

3. **Leaderboard Calculation**
   - Auto-update on accepted submissions
   - Global rankings
   - Contest rankings

4. **Better Error Handling**
   - Compilation errors
   - Runtime errors
   - Timeout handling

### Phase 3: Frontend (Week 4)

1. **React Setup**
2. **Pages**: Home, Problems List, Problem Detail, Submit, Profile
3. **Code Editor**: Monaco Editor integration
4. **Real-time Updates**: WebSocket for submission results

---

## 🎓 Chapter 6: Understanding the Flow

### The Complete User Journey (Once Everything is Built)

```
Alex opens CodeArena
  ↓
Registers account → JWT token received
  ↓
Browses problems → Sees "Two Sum" (Easy)
  ↓
Clicks problem → Reads description & examples
  ↓
Writes solution in browser editor
  ↓
Clicks "Submit"
  ↓
Backend:
  1. Saves code (status: PENDING)
  2. Returns submission_id immediately
  3. Background worker starts evaluating
  4. Runs code against 10 test cases
  5. Test case 1: PASS ✅ (42ms)
  6. Test case 2: PASS ✅ (38ms)
  7. ... all tests pass
  8. Updates status: ACCEPTED
  9. Updates leaderboard (+10 points)
  ↓
Frontend shows: "Accepted! ✅ Runtime: 42ms, Beats 87% of submissions"
  ↓
Alex's profile updates: 1 problem solved
  ↓
Leaderboard shows Alex at rank #245
```

---

## 🗺️ Where You Are Now

```
┌─────────────────────────────────────────────────────┐
│  YOU ARE HERE ⭐                                    │
│                                                      │
│  ✅ Backend architecture complete                   │
│  ✅ Authentication working                          │
│  ✅ Database models ready                           │
│  ✅ API endpoints created                           │
│  ✅ Docker environment set up                       │
│                                                      │
│  NEXT: Build the code execution engine 🚀          │
│  This is what brings your platform to life!        │
└─────────────────────────────────────────────────────┘
```

---

## 💡 Key Takeaways

1. **You've built the skeleton** - All the bones are in place
2. **You need the muscles** - Code execution is what makes it move
3. **Then the nervous system** - Real-time feedback and updates
4. **Finally the skin** - Frontend to make it beautiful

**Think of it like building a car:**
- ✅ You have the chassis (database)
- ✅ You have the frame (API structure)
- ✅ You have the steering wheel (authentication)
- ❌ You need the engine (code execution)
- ❌ You need the dashboard (frontend)

---

## 📚 Files That Matter Most

### What You've Created:
```
backend/
├── app/
│   ├── main.py              # Entry point - Routes everything
│   ├── core/
│   │   ├── config.py        # Settings (DB URL, JWT secret, etc.)
│   │   ├── database.py      # SQLAlchemy setup
│   │   └── security.py      # Password hashing, JWT creation
│   ├── models/              # Database tables (ORM)
│   │   ├── user.py          # Users table
│   │   ├── problem.py       # Problems table
│   │   ├── submission.py    # Submissions table
│   │   └── contest.py       # Contests table
│   ├── schemas/             # Request/Response validation
│   │   ├── user.py          # UserCreate, UserResponse, etc.
│   │   ├── problem.py       # ProblemCreate, ProblemResponse
│   │   └── submission.py    # SubmissionCreate, SubmissionResponse
│   └── api/v1/endpoints/    # The actual API routes
│       ├── auth.py          # /register, /login, /me
│       ├── users.py         # /users/*
│       ├── problems.py      # /problems/*
│       └── submissions.py   # /submissions/*
```

### What You Need to Create Next:
```
backend/
├── app/
│   └── services/            # NEW! Business logic
│       ├── code_executor.py      # Runs code in Docker
│       ├── submission_evaluator.py  # Judges submissions
│       └── leaderboard_service.py   # Updates rankings
└── scripts/
    └── seed_data.py         # NEW! Add sample problems
```

---

## 🎬 The End... and The Beginning

You've built an incredible foundation. The hard part (authentication, database design, API structure) is done. 

Now comes the exciting part: **making code actually run**.

**Ready to build the execution engine?** That's where CodeArena transforms from a database with an API into a real competitive programming platform! 🚀

---

*Generated on: January 23, 2026*  
*Status: Backend Setup Complete - Core Functionality Pending*
