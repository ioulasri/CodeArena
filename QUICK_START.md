# CodeArena Quick Reference Card 🚀

## Setup & Start

```bash
# One-time setup
./setup.sh

# Database
createdb codearena
psql -d codearena < backend/migrations/001_initial_schema.sql  
psql -d codearena < backend/migrations/002_puzzle_match_schema.sql

# Terminal 1: Backend
cd backend && source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd newfront_end && npm start
```

## URLs
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

## Match Flow

```
1. Login/Register
2. Choose Puzzle (Calendar)
3. Create/Join Match
4. Wait for Opponent
5. Get Unique Input
6. Solve in IDE
7. Submit Answer
8. First Correct Wins!
```

## API Endpoints

```bash
# Auth
POST /api/v1/auth/register
POST /api/v1/auth/login

# Puzzles
GET  /api/v1/matches/puzzles

# Matches  
POST /api/v1/matches/matches/create
POST /api/v1/matches/matches/join
POST /api/v1/matches/matches/{id}/start
POST /api/v1/matches/matches/{id}/submit

# Stats
GET  /api/v1/matches/stats/me
GET  /api/v1/matches/leaderboard

# WebSocket
WS   /api/v1/ws/match/{id}?token={jwt}
```

## Puzzle Types

| Day | Name | Difficulty | Description |
|-----|------|------------|-------------|
| 1 | Crystal Cave | Easy | Sum of multiples |
| 2 | Encrypted Scroll | Medium | Pattern counting |
| 3 | Magic Grid | Medium | Max path sum |
| 4 | Sequence Cipher | Hard | Find next numbers |
| 5 | Tower of Blocks | Hard | Max value removal |

## Key Files

```
Backend:
├── app/services/puzzle_generators.py    # Add new puzzles here
├── app/services/match_service.py        # Match logic
├── app/api/v1/endpoints/matches.py      # Match API
└── migrations/002_puzzle_match_schema.sql

Frontend:
├── src/pages/PuzzleMatch.jsx            # Main game UI
├── src/pages/Calendar.jsx               # Puzzle list
├── src/pages/Leaderboard.jsx            # Rankings
└── src/services/api.js                  # API client
```

## Database Tables

- `puzzles` - Puzzle definitions
- `matches` - Game sessions
- `player_puzzle_inputs` - Unique inputs
- `player_answers` - Submissions
- `match_stats` - Player statistics
- `leaderboard` - View for rankings

## Common Tasks

### Add a New Puzzle

1. Create generator in `puzzle_generators.py`
2. Add to factory
3. Insert into `puzzles` table

```python
class MyPuzzleGenerator(PuzzleGenerator):
    def generate(self, params):
        # Your logic here
        return input_data, expected_answer
```

### Customize Colors

Edit `newfront_end/src/components/Layout.css`:
- Background: `#000045`
- Text: `#ccc`
- Links: `#9f9`
- Stars: `#ffff66`

### Test API

```bash
# Get puzzles
curl http://localhost:8000/api/v1/matches/puzzles

# Create match (requires auth)
curl -X POST http://localhost:8000/api/v1/matches/matches/create \
  -H "Authorization: Bearer YOUR_JWT" \
  -H "Content-Type: application/json" \
  -d '{"puzzle_id": 1}'
```

## Troubleshooting

**Database errors?**
```bash
# Reset and re-run migrations
dropdb codearena && createdb codearena
psql -d codearena < backend/migrations/001_initial_schema.sql
psql -d codearena < backend/migrations/002_puzzle_match_schema.sql
```

**Frontend won't start?**
```bash
cd newfront_end
rm -rf node_modules package-lock.json
npm install
```

**Backend import errors?**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

## Documentation

- [PUZZLE_PLATFORM_GUIDE.md](PUZZLE_PLATFORM_GUIDE.md) - Complete guide
- [TRANSFORMATION_SUMMARY.md](TRANSFORMATION_SUMMARY.md) - What changed
- [README.md](README.md) - Project overview

---

**Ready to play? Run `./setup.sh` and start competing!** 🏆
