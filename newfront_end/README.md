# CodeArena - Competitive Puzzle Platform

An Advent of Code-style competitive puzzle platform where players race to solve unique challenges.

## Features

- **Unique Puzzle Inputs**: Each player gets different input data
- **Real-time Competition**: Live WebSocket updates during matches
- **1v1 Battles**: Challenge friends or find random opponents
- **Multiple Puzzle Types**: Math, string parsing, sequences, and more
- **Leaderboards**: Track your wins and compete for the top spot
- **Beautiful AoC-style UI**: Retro terminal aesthetic

## Getting Started

### Install Dependencies

```bash
npm install
```

### Set Environment Variables

Create a `.env` file:

```
REACT_APP_API_URL=http://localhost:8000/api/v1
```

### Run Development Server

```bash
npm start
```

The app will open at [http://localhost:3000](http://localhost:3000)

## How to Play

1. **Login**: Create an account or sign in
2. **Choose a Puzzle**: Browse the puzzle calendar
3. **Start a Match**: Create a public/private room or join an existing one
4. **Solve in Your IDE**: Copy your unique puzzle input and solve it locally
5. **Submit Answer**: Enter your answer on the website
6. **Win!**: First correct answer wins the match 🏆

## Tech Stack

- React 18
- React Router
- Axios for API calls
- WebSockets for real-time updates
- CSS with AoC-inspired design

## Available Scripts

- `npm start` - Run development server
- `npm build` - Build for production
- `npm test` - Run tests
