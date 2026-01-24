# CodeArena System Architecture

## High-Level Flow

```
┌─────────────┐         ┌─────────────┐         ┌──────────────┐
│   Player 1  │         │   Backend   │         │   Player 2   │
│             │         │             │         │              │
│  Browser    │◄───────►│   FastAPI   │◄───────►│   Browser    │
└─────────────┘         │             │         └──────────────┘
                        │  PostgreSQL │
                        │  WebSockets │
                        └─────────────┘
```

## Match Flow Sequence

```
Player 1                Backend                 Player 2
   |                       |                       |
   |──Create Match────────►|                       |
   |◄─────Room Code────────|                       |
   |                       |                       |
   |                       |◄──────Join Match──────|
   |◄──Opponent Joined────►|──────Opponent Ready──►|
   |                       |                       |
   |───Start Match────────►|◄──────Start Match─────|
   |◄──Unique Input────────|──────Unique Input────►|
   |                       |                       |
   | [Solving in IDE...]   |   [Solving in IDE...] |
   |                       |                       |
   |──Submit: "1234"──────►|                       |
   |◄──✗ Incorrect─────────|                       |
   |                       |                       |
   |──Submit: "5678"──────►|                       |
   |◄──✓ Correct & Win!────|──────Match Over──────►|
   |                       |                       |
```

## Component Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Frontend (React)                       │
├──────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │ Calendar │  │  Match   │  │Leaderboard│ │  Login   │ │
│  │  Page    │  │  Page    │  │   Page   │  │  Page    │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
│       │              │              │             │       │
│  ┌────────────────────────────────────────────────────┐  │
│  │           AuthContext (JWT State)                  │  │
│  └────────────────────────────────────────────────────┘  │
│       │              │              │             │       │
│  ┌────────────────────────────────────────────────────┐  │
│  │        API Service (Axios + WebSocket)             │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────┬───────────────────────────────────────┘
                   │
            HTTP/WebSocket
                   │
┌──────────────────┴───────────────────────────────────────┐
│                  Backend (FastAPI)                        │
├──────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │   Auth      │  │   Matches    │  │   WebSocket    │  │
│  │  Endpoints  │  │  Endpoints   │  │    Manager     │  │
│  └─────────────┘  └──────────────┘  └────────────────┘  │
│        │                 │                   │            │
│  ┌─────────────────────────────────────────────────────┐ │
│  │              Match Service                          │ │
│  │  • Create/Join Match                                │ │
│  │  • Start Match                                      │ │
│  │  • Validate Answers                                 │ │
│  └─────────────────────────────────────────────────────┘ │
│        │                                                  │
│  ┌─────────────────────────────────────────────────────┐ │
│  │         Puzzle Generator Factory                    │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐            │ │
│  │  │Crystal   │ │Sequence  │ │  Grid    │ ...        │ │
│  │  │Generator │ │Generator │ │Generator │            │ │
│  │  └──────────┘ └──────────┘ └──────────┘            │ │
│  └─────────────────────────────────────────────────────┘ │
│        │                                                  │
│  ┌─────────────────────────────────────────────────────┐ │
│  │              Models (SQLAlchemy)                    │ │
│  │  • Puzzle  • Match  • PlayerInput                   │ │
│  │  • PlayerAnswer  • MatchStats                       │ │
│  └─────────────────────────────────────────────────────┘ │
└──────────────────┬───────────────────────────────────────┘
                   │
┌──────────────────┴───────────────────────────────────────┐
│                 Database (PostgreSQL)                     │
├──────────────────────────────────────────────────────────┤
│  Tables:                                                  │
│  • users                • puzzles                         │
│  • matches              • player_puzzle_inputs            │
│  • player_answers       • match_stats                     │
│                                                           │
│  Views:                                                   │
│  • leaderboard (aggregated rankings)                      │
│                                                           │
│  Triggers:                                                │
│  • update_match_stats() on match completion               │
└───────────────────────────────────────────────────────────┘
```

## Data Flow: Create & Play Match

```
1. Create Match
   ┌──────────┐
   │ Player 1 │
   └────┬─────┘
        │ POST /matches/create {puzzle_id: 1}
        ▼
   ┌────────────────┐
   │  Backend       │
   │  • Verify user │
   │  • Check puzzle│
   │  • Create match│
   │  • Return room │
   └────┬───────────┘
        │ {match_id, room_code: "ABC123"}
        ▼
   ┌──────────┐
   │ Player 1 │ (Shows room code)
   └──────────┘

2. Join Match
   ┌──────────┐
   │ Player 2 │
   └────┬─────┘
        │ POST /matches/join {room_code: "ABC123"}
        ▼
   ┌────────────────┐
   │  Backend       │
   │  • Find match  │
   │  • Add player2 │
   │  • Status:ready│
   └────┬───────────┘
        │ {match_id, status: "ready"}
        ▼
   ┌──────────────────────┐
   │ Both Players (WS)    │
   │ "Opponent joined!"   │
   └──────────────────────┘

3. Start Match
   ┌──────────────────────┐
   │ Either Player        │
   └────┬─────────────────┘
        │ POST /matches/{id}/start
        ▼
   ┌────────────────────────────┐
   │  Backend                   │
   │  • Generate input for P1   │
   │  • Generate input for P2   │
   │  • Calculate answers       │
   │  • Save to DB              │
   │  • Start timer             │
   └────┬───────────────────────┘
        │
        ├─────► Player 1: {input: "234\n567\n891..."}
        │
        └─────► Player 2: {input: "456\n789\n123..."}

4. Submit Answer
   ┌──────────┐
   │ Player 1 │
   └────┬─────┘
        │ POST /matches/{id}/submit {answer: "1545"}
        ▼
   ┌────────────────────────────┐
   │  Backend                   │
   │  • Get expected answer     │
   │  • Compare                 │
   │  • Check if first correct  │
   │  • Update match status     │
   │  • Update stats            │
   └────┬───────────────────────┘
        │
        ├─────► Player 1: {is_correct: true, winner_id: 1}
        │
        └─────► Player 2 (WS): "Opponent solved! Match over"
```

## WebSocket Events

```
Client → Server:
• connect(match_id, token)
• player_ready
• ping

Server → Client:
• player_connected(user_id)
• player_disconnected(user_id)
• match_started(match_id, started_at)
• answer_submitted(user_id, is_correct)
• match_completed(winner_id, winner_username)
• heartbeat(timestamp)
```

## Puzzle Generation Flow

```
┌─────────────────┐
│ Match Started   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│ PuzzleGeneratorFactory      │
│ • Get generator by type     │
│   (crystal_sum, grid_path..)│
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│ Specific Generator          │
│ • Use random params         │
│ • Generate input data       │
│ • Calculate expected answer │
│ • Return (input, answer)    │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│ Save to player_puzzle_inputs│
│ • match_id                  │
│ • player_id                 │
│ • input_data                │
│ • expected_answer           │
└─────────────────────────────┘
```

## Tech Stack Overview

```
┌─────────────────────────────────────┐
│         Frontend                     │
│  • React 18                          │
│  • React Router v6                   │
│  • Axios                             │
│  • WebSocket API                     │
│  • CSS (AoC-inspired)                │
└─────────────────────────────────────┘
              │
┌─────────────────────────────────────┐
│         Backend                      │
│  • FastAPI (Python)                  │
│  • SQLAlchemy ORM                    │
│  • Pydantic schemas                  │
│  • JWT (python-jose)                 │
│  • WebSockets (native)               │
│  • bcrypt (passwords)                │
└─────────────────────────────────────┘
              │
┌─────────────────────────────────────┐
│        Database                      │
│  • PostgreSQL 14+                    │
│  • UUID support                      │
│  • JSONB columns                     │
│  • Triggers & Views                  │
└─────────────────────────────────────┘
```

## Security Flow

```
1. Register/Login
   Client → Server: {username, password}
   Server: • Hash password (bcrypt)
           • Store in DB
           • Generate JWT
   Client ← Server: {access_token, user}

2. Protected Routes
   Client → Server: Authorization: Bearer <JWT>
   Server: • Decode JWT
           • Verify signature
           • Check expiration
           • Load user from DB
   Server → Route: User object

3. WebSocket Auth
   Client → Server: WS connection + ?token=<JWT>
   Server: • Parse token from query
           • Verify JWT
           • Accept/Reject connection
```

---

This architecture provides:
- ✅ Real-time updates via WebSocket
- ✅ Secure authentication with JWT
- ✅ Fair competition with unique inputs
- ✅ Scalable puzzle generation
- ✅ Comprehensive stats tracking
