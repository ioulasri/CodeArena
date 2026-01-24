# CodeArena Developer Guide

Complete guide for extending and customizing your puzzle platform.

---

## Table of Contents

1. [Adding New Puzzle Types](#adding-new-puzzle-types)
2. [Adding New Pages](#adding-new-pages)
3. [Adding API Endpoints](#adding-api-endpoints)
4. [Database Migrations](#database-migrations)
5. [Styling Guidelines](#styling-guidelines)
6. [WebSocket Events](#websocket-events)
7. [Authentication](#authentication)
8. [Deployment](#deployment)

---

## Adding New Puzzle Types

### Step 1: Create the Generator

File: `backend/app/services/puzzle_generators.py`

```python
class YourPuzzleGenerator(PuzzleGenerator):
    """
    Your puzzle description here.
    """
    
    def __init__(self):
        self.name = "your_puzzle_type"
        self.description = """
--- Day X: Your Puzzle Title ---

Your story goes here. Use the AdventOfCode style with:
- Triple dashes for titles
- Clear problem statement
- Examples with expected output
- Hints about the solution approach
        """
    
    def generate(self, difficulty: str = 'medium') -> Tuple[Any, str]:
        """Generate unique puzzle input and expected answer"""
        
        # Generate random parameters based on difficulty
        if difficulty == 'easy':
            size = random.randint(5, 10)
        elif difficulty == 'medium':
            size = random.randint(10, 20)
        else:  # hard
            size = random.randint(20, 50)
        
        # Generate input data
        input_data = {
            'numbers': [random.randint(1, 100) for _ in range(size)],
            'target': random.randint(100, 500)
        }
        
        # Calculate expected answer
        expected_answer = str(sum(input_data['numbers']))
        
        return input_data, expected_answer
```

### Step 2: Register in Factory

Add to `PuzzleGeneratorFactory.get_generator()`:

```python
elif puzzle_type == "your_puzzle_type":
    return YourPuzzleGenerator()
```

### Step 3: Add to Database

```sql
INSERT INTO puzzles (day, title, description, generator_type, difficulty, is_active)
VALUES
(26, 'Your Puzzle Title', 'Short description here', 'your_puzzle_type', 'medium', true);
```

---

## Adding New Pages

### Step 1: Create Component

File: `newfront_end/src/pages/YourPage.jsx`

```jsx
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './YourPage.css';

const YourPage = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Your API call here
        setLoading(false);
      } catch (error) {
        console.error('Error:', error);
      }
    };
    
    fetchData();
  }, []);

  if (loading) {
    return (
      <article className="day-desc">
        <h2>Loading...</h2>
      </article>
    );
  }

  return (
    <div className="your-page-container">
      <article className="day-desc">
        <h2>--- Your Page Title ---</h2>
        <p>Your content here</p>
      </article>
    </div>
  );
};

export default YourPage;
```

### Step 2: Create Styles

File: `newfront_end/src/pages/YourPage.css`

```css
.your-page-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

.your-page-container h2 {
  color: #ffff66;
  font-size: 1.5em;
  margin-bottom: 1em;
}

.your-page-container p {
  line-height: 1.6;
  margin-bottom: 1em;
}
```

### Step 3: Add Route

File: `newfront_end/src/App.js`

```jsx
import YourPage from './pages/YourPage';

// Inside <Routes>
<Route 
  path="/your-route" 
  element={
    <ProtectedRoute>
      <Layout year="2026" navLinks={navLinks}>
        <YourPage />
      </Layout>
    </ProtectedRoute>
  } 
/>
```

### Step 4: Add to Navigation

Update `navLinks` in App.js:

```jsx
const navLinks = {
  global: [
    { href: '/', label: 'Calendar' },
    { href: '/leaderboard', label: 'Leaderboard' },
    { href: '/your-route', label: 'Your Page' },  // Add here
  ],
  event: user ? [
    { href: '#', label: user.username },
    { href: '#', label: 'Logout', onClick: logout },
  ] : [
    { href: '/login', label: 'Login' }
  ]
};
```

---

## Adding API Endpoints

### Step 1: Create Endpoint

File: `backend/app/api/v1/endpoints/your_endpoint.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.your_schema import YourResponse

router = APIRouter()

@router.get("/your-route", response_model=List[YourResponse])
async def get_your_data(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get your data with authentication required
    """
    try:
        # Your database query here
        result = await db.execute(
            select(YourModel).where(YourModel.user_id == current_user.id)
        )
        data = result.scalars().all()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/your-route", response_model=YourResponse)
async def create_your_data(
    data: YourCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create new data
    """
    new_item = YourModel(**data.dict(), user_id=current_user.id)
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item
```

### Step 2: Create Schemas

File: `backend/app/schemas/your_schema.py`

```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class YourBaseSchema(BaseModel):
    name: str
    description: Optional[str] = None

class YourCreateSchema(YourBaseSchema):
    pass

class YourResponse(YourBaseSchema):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
```

### Step 3: Register Router

File: `backend/app/api/v1/__init__.py`

```python
from app.api.v1.endpoints import your_endpoint

api_router.include_router(
    your_endpoint.router,
    prefix="/your-route",
    tags=["Your Feature"]
)
```

### Step 4: Add Frontend API Call

File: `newfront_end/src/services/api.js`

```javascript
export const yourAPI = {
  getAll: () => api.get('/your-route'),
  getById: (id) => api.get(`/your-route/${id}`),
  create: (data) => api.post('/your-route', data),
  update: (id, data) => api.put(`/your-route/${id}`, data),
  delete: (id) => api.delete(`/your-route/${id}`)
};
```

---

## Database Migrations

### Creating a Migration

File: `backend/migrations/003_your_feature.sql`

```sql
-- Add new table
CREATE TABLE IF NOT EXISTS your_table (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add indexes
CREATE INDEX idx_your_table_user_id ON your_table(user_id);
CREATE INDEX idx_your_table_status ON your_table(status);

-- Add trigger for updated_at
CREATE OR REPLACE FUNCTION update_your_table_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_your_table_timestamp
BEFORE UPDATE ON your_table
FOR EACH ROW
EXECUTE FUNCTION update_your_table_timestamp();

-- Add column to existing table
ALTER TABLE users ADD COLUMN IF NOT EXISTS new_field VARCHAR(100);

-- Seed initial data
INSERT INTO your_table (user_id, name, description)
VALUES (1, 'Example', 'Example description');
```

### Running Migrations

```bash
# Via Docker
docker exec -i codearena-db psql -U postgres -d codearena < backend/migrations/003_your_feature.sql

# Via Makefile
make db-migrate

# Or manually
psql -h localhost -U postgres -d codearena < backend/migrations/003_your_feature.sql
```

### Rollback Migration

Create: `backend/migrations/003_your_feature_rollback.sql`

```sql
-- Reverse the changes
DROP TRIGGER IF EXISTS trigger_update_your_table_timestamp ON your_table;
DROP FUNCTION IF EXISTS update_your_table_timestamp();
DROP TABLE IF EXISTS your_table CASCADE;
ALTER TABLE users DROP COLUMN IF EXISTS new_field;
```

---

## Styling Guidelines

### AdventOfCode Color Scheme

```css
/* Main Colors */
--background: #0f0f23;
--text-normal: #cccccc;
--text-bright: #ffffff;
--text-dim: #666666;

/* Accent Colors */
--green: #00cc00;        /* Success, completed */
--yellow: #ffff66;       /* Titles, emphasis */
--gold: #ffff66;         /* Stars, achievements */
--red: #ff0000;          /* Errors, warnings */
--blue: #0066ff;         /* Links */

/* Difficulty Colors */
--easy: #00cc00;         /* Green */
--medium: #ffaa00;       /* Orange */
--hard: #ff0066;         /* Red */
```

### Common Components

```css
/* Article Box (Main Content Container) */
.day-desc {
  background: rgba(15, 15, 35, 0.8);
  border: 1px solid #333;
  padding: 1.5em;
  margin-bottom: 1em;
  border-radius: 5px;
}

/* Title Style */
.day-desc h2 {
  color: #ffff66;
  font-size: 1.5em;
  margin-bottom: 0.5em;
  font-weight: normal;
}

/* Code Block */
.day-desc pre {
  background: #10101a;
  border: 1px solid #333;
  padding: 1em;
  overflow-x: auto;
  font-family: 'Source Code Pro', monospace;
  color: #ccc;
}

/* Emphasis (Stars) */
.day-desc em.star {
  color: #ffff66;
  font-style: normal;
  text-shadow: 0 0 5px #ffff66;
}

/* Links */
.day-desc a {
  color: #009900;
  text-decoration: none;
}

.day-desc a:hover {
  color: #99ff99;
}

/* Buttons */
.aoc-button {
  background: #10101a;
  border: 1px solid #333;
  color: #cccccc;
  padding: 0.5em 1em;
  font-family: 'Source Code Pro', monospace;
  cursor: pointer;
  transition: all 0.2s;
}

.aoc-button:hover {
  background: #1a1a2e;
  border-color: #666;
  color: #ffffff;
}

.aoc-button.primary {
  border-color: #00cc00;
  color: #00cc00;
}

.aoc-button.primary:hover {
  background: rgba(0, 204, 0, 0.1);
}
```

---

## WebSocket Events

### Backend: Sending Events

```python
from app.services.websocket_manager import manager

# In your endpoint or service
await manager.broadcast_to_match(
    match_id=match.id,
    event_type="custom_event",
    data={
        "message": "Your custom data",
        "timestamp": datetime.utcnow().isoformat()
    }
)
```

### Frontend: Receiving Events

```javascript
// In your component
useEffect(() => {
  const ws = createWebSocketConnection(matchId);
  
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    switch(data.type) {
      case 'custom_event':
        console.log('Custom event:', data);
        // Handle your custom event
        break;
        
      case 'match_started':
        setMatchStarted(true);
        break;
        
      case 'opponent_answered':
        setOpponentAnswered(true);
        break;
    }
  };
  
  return () => {
    if (ws.readyState === WebSocket.OPEN) {
      ws.close();
    }
  };
}, [matchId]);
```

### Adding New WebSocket Event Types

1. **Backend**: Add to `websocket_manager.py`

```python
async def notify_custom_event(self, match_id: int, data: dict):
    """Send custom event notification"""
    await self.broadcast_to_match(
        match_id=match_id,
        event_type="custom_event",
        data=data
    )
```

2. **Frontend**: Handle in component

```javascript
case 'custom_event':
  setCustomData(data);
  showNotification(data.message);
  break;
```

---

## Authentication

### Protecting Backend Endpoints

```python
from app.core.security import get_current_user
from app.models.user import User

@router.get("/protected-route")
async def protected_endpoint(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Only authenticated users can access this"""
    return {"user_id": current_user.id, "username": current_user.username}
```

### Protecting Frontend Routes

```jsx
import { ProtectedRoute } from './App';

<Route 
  path="/protected" 
  element={
    <ProtectedRoute>
      <YourProtectedPage />
    </ProtectedRoute>
  } 
/>
```

### Getting Current User in Component

```jsx
import { useAuth } from '../context/AuthContext';

const YourComponent = () => {
  const { user, isAuthenticated, logout } = useAuth();
  
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }
  
  return (
    <div>
      <p>Welcome, {user.username}!</p>
      <button onClick={logout}>Logout</button>
    </div>
  );
};
```

---

## Deployment

### Docker Deployment

```bash
# Build and start all services
docker-compose up --build -d

# Run migrations
make db-migrate

# Check logs
docker-compose logs -f

# Restart specific service
docker-compose restart backend
docker-compose restart frontend

# Stop all services
docker-compose down

# Clean slate (remove volumes)
docker-compose down -v
```

### Environment Variables

Create `.env` file in project root:

```bash
# Database
DATABASE_URL=postgresql://postgres:your_password@postgres:5432/codearena

# Backend
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=43200

# Frontend (build-time)
REACT_APP_API_URL=http://localhost:8000/api/v1
```

### Production Checklist

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Use strong database password
- [ ] Enable HTTPS (add nginx with SSL)
- [ ] Set `CORS` origins to your domain only
- [ ] Use environment-specific `.env` files
- [ ] Enable database backups
- [ ] Set up monitoring and logging
- [ ] Configure rate limiting
- [ ] Review security headers
- [ ] Test error handling

---

## Common Tasks

### Add a New Difficulty Level

1. **Database**: Update check constraint in `puzzles` table
2. **Backend**: Add to difficulty enum in schemas
3. **Frontend**: Add CSS class for the difficulty color
4. **Generator**: Add difficulty logic in `generate()` method

### Add User Profile Fields

1. **Migration**: Add column to `users` table
2. **Model**: Add field to `User` model
3. **Schema**: Add to `UserResponse` schema
4. **API**: Create endpoint to update field
5. **Frontend**: Add to user profile page

### Add Notifications

1. **Database**: Create `notifications` table
2. **Backend**: Create notification service
3. **WebSocket**: Send real-time notifications
4. **Frontend**: Add notification component
5. **Context**: Create NotificationContext for state

---

## Debugging Tips

### Backend Debugging

```bash
# Check backend logs
docker-compose logs -f backend

# Access backend container
docker exec -it codearena-backend bash

# Test API endpoint
curl -X GET http://localhost:8000/api/v1/puzzles

# Check database
docker exec -it codearena-db psql -U postgres -d codearena
\dt  # List tables
SELECT * FROM puzzles;
```

### Frontend Debugging

```bash
# Check frontend logs
docker-compose logs -f frontend

# Check build logs
docker-compose up --build frontend

# Test API calls (browser console)
fetch('http://localhost:8000/api/v1/puzzles')
  .then(r => r.json())
  .then(d => console.log(d));
```

### Database Debugging

```sql
-- Check if migrations ran
SELECT * FROM puzzles LIMIT 5;

-- Check user count
SELECT COUNT(*) FROM users;

-- Check match stats
SELECT * FROM match_stats ORDER BY matches_won DESC LIMIT 10;

-- Reset a user's stats
UPDATE users SET matches_won = 0, matches_lost = 0 WHERE username = 'testuser';
```

---

## Example: Adding a "Daily Challenge" Feature

### Complete Implementation

1. **Database Migration** (`004_daily_challenge.sql`)

```sql
CREATE TABLE daily_challenges (
    id SERIAL PRIMARY KEY,
    puzzle_id INTEGER NOT NULL REFERENCES puzzles(id),
    challenge_date DATE NOT NULL UNIQUE,
    participant_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE daily_challenge_attempts (
    id SERIAL PRIMARY KEY,
    challenge_id INTEGER NOT NULL REFERENCES daily_challenges(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    answer TEXT,
    is_correct BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,
    UNIQUE(challenge_id, user_id)
);
```

2. **Backend Model** (`models/daily_challenge.py`)

```python
from sqlalchemy import Column, Integer, Date, ForeignKey, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base

class DailyChallenge(Base):
    __tablename__ = "daily_challenges"
    
    id = Column(Integer, primary_key=True)
    puzzle_id = Column(Integer, ForeignKey("puzzles.id"))
    challenge_date = Column(Date, nullable=False, unique=True)
    participant_count = Column(Integer, default=0)
    
    puzzle = relationship("Puzzle")
    attempts = relationship("DailyChallengeAttempt", back_populates="challenge")
```

3. **Backend Endpoint** (`endpoints/daily_challenge.py`)

```python
from fastapi import APIRouter, Depends
from datetime import date

router = APIRouter()

@router.get("/daily")
async def get_daily_challenge(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()
    challenge = await db.execute(
        select(DailyChallenge)
        .where(DailyChallenge.challenge_date == today)
    )
    return challenge.scalar_one_or_none()
```

4. **Frontend Page** (`pages/DailyChallenge.jsx`)

```jsx
const DailyChallenge = () => {
  const [challenge, setChallenge] = useState(null);
  
  useEffect(() => {
    fetchDailyChallenge();
  }, []);
  
  return (
    <article className="day-desc">
      <h2>--- Daily Challenge ---</h2>
      {challenge && (
        <div>
          <h3>{challenge.puzzle.title}</h3>
          <p>{challenge.puzzle.description}</p>
        </div>
      )}
    </article>
  );
};
```

5. **Add to Navigation**

```jsx
{ href: '/daily', label: 'Daily Challenge' }
```

---

## Support

For questions or issues:
- Check logs: `docker-compose logs -f`
- Review API docs: http://localhost:8000/docs
- Database console: `docker exec -it codearena-db psql -U postgres -d codearena`

Happy coding! 🎄⭐
