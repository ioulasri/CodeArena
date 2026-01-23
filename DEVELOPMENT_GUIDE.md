# CodeArena Development Guide 🚀

> **A comprehensive guide to understanding, maintaining, and extending CodeArena**

## Table of Contents

1. [Understanding the Big Picture](#1-understanding-the-big-picture)
2. [Core Technologies Deep Dive](#2-core-technologies-deep-dive)
3. [Architecture Breakdown](#3-architecture-breakdown)
4. [Development Workflow](#4-development-workflow)
5. [Key Concepts You Need to Know](#5-key-concepts-you-need-to-know)
6. [Common Tasks & How-Tos](#6-common-tasks--how-tos)
7. [Troubleshooting Guide](#7-troubleshooting-guide)
8. [Extending the Platform](#8-extending-the-platform)
9. [Learning Path](#9-learning-path)
10. [Next Steps & Ideas](#10-next-steps--ideas)

---

## 1. Understanding the Big Picture

### What is CodeArena?

CodeArena is a **competitive programming platform** where users can:
- Browse coding problems (like LeetCode/HackerRank)
- Write solutions in multiple languages (Python, JavaScript, Java, C++)
- Submit code for automated testing
- See their submission history and results

### The 30,000-foot View

```
┌─────────────────────────────────────────────────────────────┐
│                         USER'S PHONE/COMPUTER                │
│                                                               │
│  Browser ──────> React App (Terminal-styled UI)             │
│                     ↓ HTTP Requests                          │
└─────────────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────────┐
│                    DOCKER COMPOSE NETWORK                    │
│                                                               │
│  ┌─────────────┐     ┌──────────────┐    ┌──────────────┐  │
│  │   Nginx     │     │   FastAPI    │    │  PostgreSQL  │  │
│  │  (Frontend) │────>│   (Backend)  │───>│  (Database)  │  │
│  │  Port 3000  │     │  Port 8000   │    │  Port 5432   │  │
│  └─────────────┘     └──────────────┘    └──────────────┘  │
│                             │                                │
│                             ↓                                │
│                      ┌─────────────┐                        │
│                      │   Docker    │                        │
│                      │   Socket    │                        │
│                      └─────────────┘                        │
│                             │                                │
│                             ↓                                │
│                    Creates Containers                        │
│                    for Code Execution                        │
└─────────────────────────────────────────────────────────────┘
```

### Why These Technologies?

**Frontend - React:**
- ✅ Component-based (easy to maintain)
- ✅ Large ecosystem (tons of libraries)
- ✅ Fast and responsive user experience
- ❌ Requires build step (not a problem with Docker)

**Backend - FastAPI:**
- ✅ Modern Python framework
- ✅ Automatic API documentation (Swagger)
- ✅ Type hints for better code quality
- ✅ Async support (handles many requests)
- ✅ Easy to learn if you know Python

**Database - PostgreSQL:**
- ✅ Reliable and battle-tested
- ✅ Great with complex queries
- ✅ ACID compliant (data integrity)
- ✅ Free and open source

**Containerization - Docker:**
- ✅ Consistent environment everywhere
- ✅ Isolates code execution (security)
- ✅ Easy deployment
- ✅ Works the same on Mac, Linux, Windows

---

## 2. Core Technologies Deep Dive

### 2.1 Docker Basics (Must Know!)

**What is Docker?**
Think of Docker like a virtual machine, but lighter. It packages your app and all its dependencies into a "container."

**Key Concepts:**

```yaml
# docker-compose.yml - This is your orchestrator
services:
  backend:
    build:                    # How to build this container
      context: .              # Where to find files
      dockerfile: docker/backend.dockerfile
    ports:
      - "8000:8000"          # Host:Container port mapping
    volumes:
      - ./backend:/app       # Live sync code changes
    environment:             # Environment variables
      DATABASE_URL: postgresql://...
```

**Important Docker Commands:**

```bash
# Start everything
docker-compose up -d

# Rebuild after code changes
docker-compose build <service>

# View logs
docker-compose logs -f <service>

# Stop everything
docker-compose down

# Execute command in container
docker-compose exec <service> <command>

# Check running containers
docker-compose ps
```

**When to Rebuild:**
- ✅ Python dependencies change (`requirements.txt`)
- ✅ React dependencies change (`package.json`)
- ✅ Dockerfile changes
- ❌ Python code changes (volume-mounted, no rebuild needed)
- ❌ React code changes in dev (use `npm start`)
- ✅ React code changes for production (needs rebuild)

### 2.2 FastAPI Backend

**File Structure:**
```
backend/
├── app/
│   ├── main.py              # Entry point, CORS, routes
│   ├── database.py          # Database connection
│   ├── models/              # Database models (tables)
│   │   ├── user.py
│   │   ├── problem.py
│   │   └── submission.py
│   ├── schemas/             # Pydantic models (validation)
│   │   ├── user.py
│   │   └── problem.py
│   ├── routers/             # API endpoints
│   │   ├── auth.py          # Login, register
│   │   ├── problems.py      # Get problems
│   │   └── submissions.py   # Submit code
│   └── services/
│       └── code_executor.py # Runs user code safely
└── requirements.txt
```

**Key Concepts:**

**1. Models (Database Tables):**
```python
# models/user.py
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
```
→ This creates a `users` table in PostgreSQL

**2. Schemas (Data Validation):**
```python
# schemas/user.py
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
```
→ Validates incoming data before saving

**3. Routers (API Endpoints):**
```python
# routers/auth.py
@router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Create user logic
    return {"message": "User created"}
```
→ Accessible at: `POST http://localhost:8000/api/v1/auth/register`

**4. Dependencies:**
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```
→ Manages database connections automatically

### 2.3 React Frontend

**File Structure:**
```
frontend/
├── public/
│   ├── index.html
│   └── debug.html          # Diagnostic page
├── src/
│   ├── App.js              # Main component, routing
│   ├── App.css             # Global styles
│   ├── components/
│   │   ├── Login.js        # Login/Register UI
│   │   ├── Login.css
│   │   ├── Terminal.js     # Main app UI
│   │   └── Terminal.css
│   └── index.js            # Entry point
└── package.json
```

**Key React Concepts:**

**1. Components:**
```javascript
function Login({ onLogin }) {
    const [username, setUsername] = useState('');
    // Component logic
    return <div>UI here</div>
}
```

**2. State (Data that Changes):**
```javascript
const [token, setToken] = useState(null);
// token is the value
// setToken is how you update it
```

**3. Effects (Side Effects):**
```javascript
useEffect(() => {
    // Runs when token changes
    fetch('/api/auth/me')
}, [token]);  // Dependencies
```

**4. Props (Passing Data):**
```javascript
<Login onLogin={handleLogin} />
// onLogin is a prop (function passed to child)
```

### 2.4 Environment Variables

**Critical for Network Access!**

```bash
# React uses REACT_APP_ prefix
REACT_APP_API_URL=http://192.168.100.2:8000

# Build-time vs Runtime:
# React: Build-time (must rebuild to change)
# FastAPI: Runtime (just restart container)
```

**How it works:**
```javascript
// In React code:
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// During build (npm run build):
// - Replaces process.env.REACT_APP_API_URL with actual value
// - Bundles it into JavaScript files
// - That's why you need to rebuild after changing it!
```

---

## 3. Architecture Breakdown

### 3.1 Authentication Flow

```mermaid
sequenceDiagram
    User->>React: Enters username/password
    React->>FastAPI: POST /api/v1/auth/login
    FastAPI->>Database: Check credentials
    Database-->>FastAPI: User found ✓
    FastAPI->>FastAPI: Generate JWT token
    FastAPI-->>React: Return token
    React->>React: Store in localStorage
    React->>FastAPI: GET /api/v1/auth/me (with token)
    FastAPI->>FastAPI: Verify token
    FastAPI-->>React: User data
    React->>React: Show main app
```

**JWT (JSON Web Token) Explained:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTY5...
│                                        │                                    │
│         Header                         │         Payload                    │  Signature
│    (Algorithm: HS256)                  │    (user: "admin")                 │  (Secret Key)
```

- Not encrypted (anyone can decode)
- But signed (can't be tampered with)
- Contains expiration time
- Stateless (backend doesn't store it)

### 3.2 Code Execution Flow

```mermaid
sequenceDiagram
    User->>React: Submits code
    React->>FastAPI: POST /api/v1/submissions
    FastAPI->>Database: Save submission (PENDING)
    FastAPI->>Background Task: Execute code
    Background Task->>Docker: Create container (python:3.11)
    Docker->>Container: Run user code
    Container->>Container: Execute with test cases
    Container-->>Docker: Results (stdout, stderr, exit code)
    Docker-->>Background Task: Execution complete
    Background Task->>Database: Update submission (ACCEPTED/WRONG_ANSWER)
    User->>React: Polls for results
    React->>FastAPI: GET /api/v1/submissions/{id}
    FastAPI-->>React: Updated status
```

**Why Docker for Code Execution?**

```python
# services/code_executor.py
client.containers.run(
    image="python:3.11-slim",
    command=["python", "-c", user_code],
    mem_limit="128m",          # Limit memory
    cpu_period=100000,         # Limit CPU
    cpu_quota=50000,           # 50% of one CPU
    network_disabled=True,     # No internet access
    remove=True,               # Auto-cleanup
    timeout=10                 # 10 second max
)
```

**Security Benefits:**
- ✅ Isolated from main system
- ✅ Resource limits (can't crash server)
- ✅ No network access (can't make external calls)
- ✅ Read-only filesystem (mostly)
- ✅ Timeout protection (can't run forever)

---

## 4. Development Workflow

### 4.1 Making Changes

**Backend Changes (Python):**
```bash
# 1. Edit Python files
vim backend/app/routers/problems.py

# 2. Changes reflect immediately (volume-mounted + --reload)
# No rebuild needed!

# 3. Check logs
docker-compose logs -f backend
```

**Frontend Changes (Development):**
```bash
# Option 1: Work outside Docker (faster)
cd frontend
npm start  # Opens at localhost:3000

# Option 2: Rebuild container
docker-compose build frontend
docker-compose up -d frontend
```

**Frontend Changes (Production):**
```bash
# Always rebuild
docker-compose build frontend
docker-compose up -d frontend

# Verify new build
docker-compose exec frontend sh -c "cat /usr/share/nginx/html/static/js/main.*.js | grep 'YOUR_CHANGE'"
```

### 4.2 Database Changes

**Adding a New Field:**

```python
# 1. Edit model
# models/problem.py
class Problem(Base):
    # ... existing fields ...
    hints = Column(Text)  # NEW FIELD
```

```bash
# 2. Create migration
docker-compose exec backend alembic revision --autogenerate -m "Add hints to problems"

# 3. Apply migration
docker-compose exec backend alembic upgrade head

# 4. Verify
docker-compose exec postgres psql -U postgres -d codearena -c "\d problems"
```

**Alternative (Reset Everything):**
```bash
# WARNING: Deletes all data!
docker-compose down -v
docker-compose up -d
docker-compose exec backend python -m app.database
docker-compose exec backend python backend/scripts/seed_data.py
```

### 4.3 Git Workflow

```bash
# 1. Create feature branch
git checkout -b feature/your-feature-name

# 2. Make changes and commit
git add file.py
git commit -m "feat: add feature description"

# 3. Push to GitHub
git push -u origin feature/your-feature-name

# 4. Create Pull Request on GitHub
# Review, test, merge to main

# 5. Update local main
git checkout main
git pull origin main

# 6. Delete feature branch
git branch -d feature/your-feature-name
```

**Commit Message Convention:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `refactor:` - Code restructuring
- `test:` - Adding tests
- `chore:` - Maintenance

---

## 5. Key Concepts You Need to Know

### 5.1 Async/Await in Python

```python
# Synchronous (blocks)
def get_user(user_id):
    user = db.query(User).filter(User.id == user_id).first()
    return user

# Asynchronous (doesn't block)
async def get_user(user_id):
    user = await db.query(User).filter(User.id == user_id).first()
    return user
```

**When to use async?**
- ✅ Database queries
- ✅ External API calls
- ✅ File I/O
- ❌ Pure computation (CPU-bound)

### 5.2 Database Relationships

```python
# One-to-Many (User -> Submissions)
class User(Base):
    submissions = relationship("Submission", back_populates="user")

class Submission(Base):
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="submissions")

# Usage:
user = db.query(User).first()
for submission in user.submissions:
    print(submission.status)
```

### 5.3 CORS (Cross-Origin Resource Sharing)

**Why do we need it?**

```
Browser at http://192.168.100.2:3000 (Frontend)
    ↓
    Tries to fetch http://192.168.100.2:8000/api/... (Backend)
    ↓
    Browser blocks it! (Different origin)
    ↓
    Backend must send CORS headers:
    access-control-allow-origin: http://192.168.100.2:3000
    ↓
    Browser allows it ✓
```

**Common CORS Issues:**
```python
# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",          # Development
        "http://192.168.100.2:3000",      # Network access
        # Add your production domain here
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 5.4 Docker Networking

**Container Names vs Hosts:**

```yaml
# Inside docker-compose network:
DATABASE_URL: postgresql://postgres:postgres@postgres:5432/codearena
                                              ↑
                                        Service name (not localhost!)

# From your computer:
postgresql://postgres:postgres@localhost:5432/codearena
                                   ↑
                             Now it's localhost
```

**Port Mapping:**
```yaml
ports:
  - "3000:80"
    ↑     ↑
    Host  Container
```
- Access from outside: `http://localhost:3000`
- Inside container: port `80`

---

## 6. Common Tasks & How-Tos

### 6.1 Add a New API Endpoint

```python
# 1. Create router function
# backend/app/routers/problems.py

@router.get("/problems/{problem_id}/hints")
async def get_hints(
    problem_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return {"hints": problem.hints}
```

```javascript
// 2. Call from frontend
// frontend/src/components/Terminal.js

const fetchHints = async (problemId) => {
    const response = await fetch(`${API_URL}/api/v1/problems/${problemId}/hints`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await response.json();
    setHints(data.hints);
};
```

### 6.2 Add a New Programming Language

```python
# 1. Add to code executor
# backend/app/services/code_executor.py

LANGUAGE_CONFIGS = {
    "rust": {
        "image": "rust:1.70-slim",
        "file_ext": ".rs",
        "compile_cmd": ["rustc", "solution.rs"],
        "run_cmd": ["./solution"],
    }
}

# 2. Update problem model
# backend/app/models/problem.py
supported_languages = ["python", "javascript", "java", "cpp", "rust"]

# 3. Add to frontend dropdown
# frontend/src/components/Terminal.js
<option value="rust">Rust</option>
```

### 6.3 Add Authentication to an Endpoint

```python
from app.routers.auth import get_current_user

@router.get("/protected")
async def protected_route(
    current_user: User = Depends(get_current_user)  # Add this!
):
    return {"message": f"Hello {current_user.username}"}
```

### 6.4 Change Network IP Address

```yaml
# 1. Update docker-compose.yml
services:
  frontend:
    build:
      args:
        REACT_APP_API_URL: http://NEW_IP:8000  # Change here

# 2. Update CORS
# backend/app/main.py
allow_origins=[
    "http://NEW_IP:3000",  # Change here
]

# 3. Rebuild
docker-compose build frontend
docker-compose restart backend
docker-compose up -d frontend
```

---

## 7. Troubleshooting Guide

### 7.1 "Cannot connect to Docker daemon"

```bash
# Check if Docker is running
docker ps

# Start Docker Desktop (Mac/Windows)
# or
sudo systemctl start docker  # Linux
```

### 7.2 "Port already in use"

```bash
# Find what's using port 8000
lsof -i :8000

# Kill it
kill -9 <PID>

# Or change port in docker-compose.yml
ports:
  - "8001:8000"  # Use 8001 instead
```

### 7.3 "frontend | 502 Bad Gateway"

**Cause:** Frontend trying to reach backend before it's ready

```bash
# Check backend logs
docker-compose logs backend

# Wait for: "Uvicorn running on http://0.0.0.0:8000"

# Restart frontend
docker-compose restart frontend
```

### 7.4 "Module not found" in Backend

```bash
# Rebuild after adding dependency
docker-compose build backend
docker-compose up -d backend
```

### 7.5 Login Redirects Back Immediately

**Common causes:**
1. **Wrong API URL in React build**
   ```bash
   # Check what's in the build
   docker-compose exec frontend sh -c "grep -o 'API_URL' /usr/share/nginx/html/static/js/*.js"
   
   # Rebuild if wrong
   docker-compose build frontend
   docker-compose up -d frontend
   ```

2. **CORS blocking requests**
   ```bash
   # Check CORS headers
   curl -H "Origin: http://192.168.100.2:3000" http://192.168.100.2:8000/api/v1/auth/me -v
   
   # Look for: access-control-allow-origin
   ```

3. **Token verification failing**
   ```javascript
   // Check browser console (F12)
   // Look for: "Token verification error"
   ```

### 7.6 Code Execution Hangs

```bash
# Check Docker socket is mounted
docker-compose exec backend ls -la /var/run/docker.sock

# Should show: srw-rw---- docker.sock

# If not, add to docker-compose.yml:
volumes:
  - /var/run/docker.sock:/var/run/docker.sock
```

---

## 8. Extending the Platform

### 8.1 Ideas for New Features

**Easy (Weekend Project):**
- [ ] User profiles with bio and avatar
- [ ] Problem difficulty filter
- [ ] Copy code to clipboard button
- [ ] Dark/light theme toggle
- [ ] Export submission history as CSV

**Medium (1-2 weeks):**
- [ ] Real-time leaderboard
- [ ] Submission statistics and charts
- [ ] Code syntax highlighting
- [ ] Problem tags and categories
- [ ] Search problems by keyword
- [ ] Time and memory limits per problem
- [ ] Multiple test cases per problem

**Advanced (Month+):**
- [ ] Live contests with countdown timer
- [ ] Peer code review system
- [ ] Discussion forum per problem
- [ ] Video tutorials integration
- [ ] AI-powered hint system
- [ ] Multiplayer code battles
- [ ] Integration with GitHub/GitLab

### 8.2 Performance Optimizations

**Database:**
```python
# Add indexes for common queries
class Problem(Base):
    __tablename__ = "problems"
    __table_args__ = (
        Index('idx_difficulty', 'difficulty'),
        Index('idx_category', 'category'),
    )
```

**Backend:**
```python
# Cache frequently accessed data
from functools import lru_cache

@lru_cache(maxsize=100)
def get_problem(problem_id: int):
    # Cached for 100 most recent problems
    pass
```

**Frontend:**
```javascript
// Lazy load components
const Terminal = React.lazy(() => import('./components/Terminal'));

// Use React.memo for expensive components
const ProblemList = React.memo(({ problems }) => {
    // Only re-renders if problems change
});
```

### 8.3 Security Enhancements

**1. Rate Limiting:**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/login")
@limiter.limit("5/minute")  # Max 5 attempts per minute
async def login():
    pass
```

**2. Input Validation:**
```python
from pydantic import validator

class ProblemCreate(BaseModel):
    title: str
    
    @validator('title')
    def title_must_be_safe(cls, v):
        if len(v) > 100:
            raise ValueError('Title too long')
        if '<script>' in v.lower():
            raise ValueError('Invalid characters')
        return v
```

**3. Better Password Security:**
```python
# Current: bcrypt (good)
# Better: Add password complexity requirements

from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # More rounds = slower = more secure
)
```

---

## 9. Learning Path

### 9.1 If You're New to Docker

**Resources:**
1. [Docker Official Tutorial](https://www.docker.com/101-tutorial/) (2 hours)
2. [Docker Compose Documentation](https://docs.docker.com/compose/) (Read: Getting Started)
3. YouTube: "Docker Tutorial for Beginners" by TechWorld with Nana

**Practice:**
```bash
# Experiment with commands
docker-compose logs -f backend
docker-compose exec backend bash
docker-compose down && docker-compose up -d
```

### 9.2 If You're New to FastAPI

**Resources:**
1. [FastAPI Official Tutorial](https://fastapi.tiangolo.com/tutorial/) (Best resource!)
2. Read through our codebase in this order:
   - `backend/app/main.py` - Entry point
   - `backend/app/routers/auth.py` - Authentication
   - `backend/app/models/user.py` - Database models
   - `backend/app/services/code_executor.py` - Code execution

**Practice:**
```python
# Try adding a simple endpoint
@router.get("/hello/{name}")
async def hello(name: str):
    return {"message": f"Hello {name}!"}
```

### 9.3 If You're New to React

**Resources:**
1. [React Official Tutorial](https://react.dev/learn) (Excellent!)
2. [React Hooks](https://react.dev/reference/react) - useState, useEffect
3. YouTube: "React Hooks Course" by Web Dev Simplified

**Practice:**
```javascript
// Create a simple counter component
function Counter() {
    const [count, setCount] = useState(0);
    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={() => setCount(count + 1)}>
                Increment
            </button>
        </div>
    );
}
```

### 9.4 Understanding the Full Stack

**Read in this order:**
1. **Week 1:** Docker + Docker Compose
2. **Week 2:** FastAPI basics (routing, models, schemas)
3. **Week 3:** React basics (components, state, props)
4. **Week 4:** Database (PostgreSQL, SQLAlchemy)
5. **Week 5:** Authentication (JWT, password hashing)
6. **Week 6:** Put it all together (trace a request end-to-end)

**Exercise: Trace a Login Request**

1. User clicks "Login" in React
2. `Login.js` calls `handleSubmit()`
3. Sends POST to `/api/v1/auth/login`
4. Nginx forwards to FastAPI
5. `backend/app/routers/auth.py` → `login()` function
6. Checks password with `verify_password()`
7. Creates JWT token with `create_access_token()`
8. Returns token to React
9. React stores in `localStorage`
10. React updates state → shows Terminal component

Do this exercise with other features!

---

## 10. Next Steps & Ideas

### 10.1 Immediate Next Steps (Today!)

1. **Try the debug page:** `http://192.168.100.2:3000/debug.html`
   - Understand what it's testing
   - Add more tests to it

2. **Make a small change:**
   ```python
   # Change the welcome message in Terminal.js
   <p className="welcome-text">
       > Welcome to CodeArena, {user.username}! 🚀
   </p>
   ```

3. **Add your first problem:**
   ```sql
   docker-compose exec postgres psql -U postgres codearena
   
   INSERT INTO problems (title, description, difficulty, category, created_at)
   VALUES (
       'Sum of Two Numbers',
       'Write a function that takes two numbers and returns their sum.',
       'Easy',
       'Math',
       NOW()
   );
   ```

### 10.2 This Week

1. **Read the entire codebase** - You understand more than you think!
2. **Break something on purpose** - Then fix it (best way to learn)
3. **Add a feature:**
   - User statistics page
   - Problem bookmarking
   - Code templates

### 10.3 This Month

1. **Deploy to production:**
   - DigitalOcean ($5/month)
   - Heroku (free tier)
   - AWS EC2

2. **Add tests:**
   ```python
   # backend/tests/test_auth.py
   def test_login():
       response = client.post("/api/v1/auth/login", json={
           "username": "admin",
           "password": "admin123"
       })
       assert response.status_code == 200
       assert "access_token" in response.json()
   ```

3. **Improve the UI:**
   - Better error messages
   - Loading states
   - Animations

### 10.4 Dream Big (Future)

- **Mobile app** (React Native)
- **VS Code extension**
- **Browser extension** (auto-submit to CodeArena)
- **Integration with universities** (assignments platform)
- **Competitive programming contests**
- **Company coding challenges** (recruitment tool)

---

## Appendix A: Full Tech Stack Reference

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Frontend | React | 18.2.0 | UI framework |
| Frontend | Nginx | Alpine | Web server |
| Backend | FastAPI | Latest | API framework |
| Backend | SQLAlchemy | Latest | ORM |
| Backend | Pydantic | Latest | Data validation |
| Backend | python-jose | Latest | JWT tokens |
| Backend | passlib | Latest | Password hashing |
| Backend | Docker SDK | 7.0.0 | Code execution |
| Database | PostgreSQL | 15 | Data storage |
| Container | Docker | Latest | Containerization |
| Orchestration | Docker Compose | 3.8 | Multi-container management |

## Appendix B: Environment Variables Reference

### Backend
```env
DATABASE_URL=postgresql://user:pass@host:port/dbname
SECRET_KEY=your-secret-key-for-jwt
API_HOST=0.0.0.0
API_PORT=8000
```

### Frontend
```env
REACT_APP_API_URL=http://192.168.100.2:8000
```

## Appendix C: Useful Commands Cheat Sheet

```bash
# Development
docker-compose up -d              # Start all services
docker-compose logs -f <service>  # Watch logs
docker-compose exec <service> bash # Enter container
docker-compose restart <service>  # Restart one service

# Database
docker-compose exec postgres psql -U postgres codearena
docker-compose exec backend alembic upgrade head

# Cleanup
docker-compose down               # Stop all
docker-compose down -v            # Stop all + delete volumes
docker system prune -a            # Clean everything

# Git
git status                        # Check changes
git add .                         # Stage all
git commit -m "message"           # Commit
git push                          # Push to GitHub
```

---

## Final Thoughts

**You Don't Need to Know Everything!**

The beauty of modern web development is that you can:
- Learn one part at a time
- Google things as needed
- Use AI assistants (like me!)
- Refer back to this guide

**Start Small:**
1. Pick ONE feature to add
2. Trace through the code
3. Make the change
4. Test it
5. Commit it

**Get Stuck? That's Normal!**
- Read error messages carefully
- Check logs: `docker-compose logs`
- Use the debug page
- Google the error
- Ask for help

**You've Got This! 🚀**

You have a working, production-ready platform. Everything else is just building on top of this foundation.

---

**Questions? Issues?**
- Check logs first
- Use the debug page
- Review this guide
- Google specific errors
- Ask in relevant communities (r/FastAPI, r/reactjs, r/docker)

**Happy Coding! 💻**

*Last Updated: January 23, 2026*
