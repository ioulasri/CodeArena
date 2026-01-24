# CodeArena - Competitive Puzzle Platform Setup Guide

## 🎮 What Changed?

Your platform has been transformed from a LeetCode-style code executor to an **Advent of Code-inspired competitive puzzle platform**! 

### Key Features:
- ✅ Unique puzzle inputs for each player (no code submission needed!)
- ✅ Real-time 1v1 matches with WebSocket updates
- ✅ 5 fun puzzle types with generators
- ✅ Beautiful AoC-style retro UI
- ✅ Private rooms to challenge friends
- ✅ Global leaderboards with stats tracking
- ✅ Players solve in their own IDE and submit answers

## 🚀 Quick Start

### 1. Database Setup

Run the new migration to create the puzzle tables:

```bash
cd backend
psql -U your_user -d codearena < migrations/002_puzzle_match_schema.sql
```

This creates:
- `puzzles` - Puzzle definitions with generators
- `matches` - 1v1 game matches
- `player_puzzle_inputs` - Unique inputs per player
- `player_answers` - Answer submissions
- `match_stats` - Player statistics
- Leaderboard view

### 2. Backend Setup

Install Python dependencies (if not already installed):

```bash
cd backend
pip install -r requirements.txt
```

Start the backend:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend runs at: `http://localhost:8000`
API Docs: `http://localhost:8000/docs`

### 3. Frontend Setup

Install Node.js dependencies:

```bash
cd newfront_end
npm install
```

Start the development server:

```bash
npm start
```

Frontend runs at: `http://localhost:3000`

## 📁 What's New?

### Backend Files Created:

```
backend/
├── migrations/
│   └── 002_puzzle_match_schema.sql       # New database schema
├── app/
│   ├── models/
│   │   └── puzzle.py                     # Puzzle, Match, Stats models
│   ├── schemas/
│   │   └── puzzle.py                     # API schemas
│   ├── services/
│   │   ├── puzzle_generators.py          # 5 puzzle generators
│   │   ├── match_service.py              # Match logic
│   │   └── websocket_manager.py          # Real-time updates
│   └── api/v1/endpoints/
│       ├── matches.py                    # Match API endpoints
│       └── websocket.py                  # WebSocket endpoint
```

### Frontend Files Created:

```
newfront_end/
├── package.json                          # Dependencies
├── src/
│   ├── context/
│   │   └── AuthContext.jsx              # Authentication
│   ├── services/
│   │   └── api.js                       # API client
│   ├── pages/
│   │   ├── Calendar.jsx                 # Puzzle list
│   │   ├── PuzzleMatch.jsx              # Main game screen
│   │   ├── Leaderboard.jsx              # Rankings
│   │   └── Login.jsx                    # Auth
│   └── App.js                           # Routing
```

## 🎯 How to Play

### For Players:

1. **Create an account** at `/login`
2. **Browse puzzles** on the calendar
3. **Start a match**:
   - Quick Match: Find random opponent
   - Private Room: Get a code to share with friends
4. **Get unique puzzle input** when match starts
5. **Solve in your IDE** (Python, JavaScript, whatever!)
6. **Submit answer** on the website
7. **First correct answer wins!** 🏆

### Example Workflow:

```python
# Day 1: Crystal Cave Numbers
# Input: List of numbers
# Task: Sum of multiples of 3 or 5

numbers = [234, 567, 891, ...]  # Your unique input
result = sum(n for n in numbers if n % 3 == 0 or n % 5 == 0)
print(result)  # Submit this as your answer!
```

## 🧩 Available Puzzles

1. **Crystal Cave Numbers** (Easy) - Sum of multiples
2. **Encrypted Scroll** (Medium) - Pattern counting
3. **Magic Grid** (Medium) - Path finding
4. **Sequence Cipher** (Hard) - Number sequences
5. **Tower of Blocks** (Hard) - Maximum subarray

## 🔧 API Endpoints

### Puzzles
- `GET /api/v1/matches/puzzles` - List all puzzles
- `GET /api/v1/matches/puzzles/{id}` - Get puzzle details

### Matches
- `POST /api/v1/matches/matches/create` - Create match
- `POST /api/v1/matches/matches/join` - Join match
- `POST /api/v1/matches/matches/{id}/start` - Start match
- `POST /api/v1/matches/matches/{id}/submit` - Submit answer
- `GET /api/v1/matches/matches/{id}` - Get match details

### Stats
- `GET /api/v1/matches/stats/me` - Your stats
- `GET /api/v1/matches/leaderboard` - Global rankings
- `GET /api/v1/matches/matches/user/history` - Match history

### WebSocket
- `WS /api/v1/ws/match/{match_id}?token={jwt}` - Live updates

## 🎨 UI Customization

The UI uses Advent of Code's aesthetic. To customize:

1. **Colors**: Edit `/newfront_end/src/components/Layout.css`
   - Background: `#000045` (dark blue)
   - Text: `#ccc` (light gray)
   - Links: `#9f9` (bright green)
   - Stars: `#ffff66` (yellow)

2. **Components**: All styled in their respective CSS files
3. **Animations**: Star effects, pulses, victory celebrations

## 🐛 Troubleshooting

### Database Issues
```bash
# Reset database
psql -U your_user -d codearena -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
# Re-run migrations
psql -U your_user -d codearena < migrations/001_initial_schema.sql
psql -U your_user -d codearena < migrations/002_puzzle_match_schema.sql
```

### CORS Issues
Backend CORS is configured for:
- `http://localhost:3000`
- `http://127.0.0.1:3000`

Update in `backend/app/main.py` if needed.

### WebSocket Connection
Make sure backend supports WebSockets (FastAPI does by default).

## 📦 Production Deployment

### Backend
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend
```bash
cd newfront_end
npm run build
# Serve the build/ folder with nginx or similar
```

## 🎉 What's Next?

### Ideas to Extend:
- [ ] Add more puzzle types
- [ ] Tournament mode (multiple rounds)
- [ ] Puzzle difficulty ratings
- [ ] Daily challenges
- [ ] Team matches (2v2, 3v3)
- [ ] Puzzle creator tools
- [ ] Discord integration
- [ ] Custom puzzle submissions

## 📚 Tech Stack

**Backend:**
- FastAPI (Python)
- PostgreSQL
- SQLAlchemy
- WebSockets
- JWT Authentication

**Frontend:**
- React 18
- React Router
- Axios
- WebSocket API
- CSS (AoC-inspired)

## 🤝 Need Help?

Check out:
- Backend API docs: `http://localhost:8000/docs`
- Frontend README: `newfront_end/README.md`
- Database schema: `backend/migrations/002_puzzle_match_schema.sql`

---

**Have fun and may the fastest solver win!** 🏆⚔️
