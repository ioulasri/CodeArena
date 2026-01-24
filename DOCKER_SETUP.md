# Docker Compose Setup for CodeArena

## Quick Start with Docker

Run the entire platform with a single command!

```bash
docker-compose up --build
```

This will start:
- PostgreSQL database (port 5432)
- Backend API (port 8000)
- New puzzle frontend (port 3000)

Access the app at: **http://localhost:3000**

## Services

### Database (postgres)
- **Image**: postgres:15-alpine
- **Port**: 5432
- **Database**: codearena
- **User**: postgres
- **Password**: postgres

### Backend (FastAPI)
- **Port**: 8000
- **API Docs**: http://localhost:8000/docs
- **Hot reload**: Enabled
- **Volume**: ./backend mounted to /app

### Frontend (React - NEW!)
- **Port**: 3000 (served via nginx)
- **Build**: Production build of newfront_end
- **API URL**: http://localhost:8000/api/v1

## Commands

```bash
# Start all services
docker-compose up

# Start with rebuild
docker-compose up --build

# Start in background
docker-compose up -d

# Stop all services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Restart a service
docker-compose restart backend
```

## Database Setup

The database tables need to be created on first run:

```bash
# Method 1: Via Docker exec
docker-compose exec postgres psql -U postgres -d codearena -f /docker-entrypoint-initdb.d/001_initial_schema.sql

# Method 2: Copy migrations and run
docker cp backend/migrations/001_initial_schema.sql codearena-db:/tmp/
docker cp backend/migrations/002_puzzle_match_schema.sql codearena-db:/tmp/
docker-compose exec postgres psql -U postgres -d codearena -f /tmp/001_initial_schema.sql
docker-compose exec postgres psql -U postgres -d codearena -f /tmp/002_puzzle_match_schema.sql

# Method 3: From your host (if you have psql)
psql -h localhost -U postgres -d codearena < backend/migrations/001_initial_schema.sql
psql -h localhost -U postgres -d codearena < backend/migrations/002_puzzle_match_schema.sql
```

## Environment Variables

You can customize via docker-compose.yml or create a .env file:

```env
# Database
POSTGRES_DB=codearena
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password

# Backend
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/codearena
SECRET_KEY=your-secret-key-here
API_HOST=0.0.0.0
API_PORT=8000

# Frontend (build-time)
REACT_APP_API_URL=http://localhost:8000/api/v1
```

## Accessing Services

Once running:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: localhost:5432

## Troubleshooting

### Frontend not loading?
```bash
# Rebuild frontend
docker-compose up --build frontend
```

### Database connection issues?
```bash
# Check postgres health
docker-compose ps
docker-compose logs postgres

# Wait for health check to pass
# It takes ~10 seconds for postgres to be ready
```

### Backend errors?
```bash
# Check backend logs
docker-compose logs backend

# Restart backend
docker-compose restart backend
```

### Port conflicts?
If ports 3000, 8000, or 5432 are already in use, edit docker-compose.yml:
```yaml
ports:
  - "3001:80"    # Change 3000 to 3001
  - "8001:8000"  # Change 8000 to 8001
  - "5433:5432"  # Change 5432 to 5433
```

## Development vs Production

### Development (current setup)
- Hot reload enabled
- Source code mounted as volumes
- Debug logs
- Development database

### Production (recommended changes)
1. Use environment-specific .env files
2. Remove volume mounts
3. Use production database
4. Set strong SECRET_KEY
5. Enable HTTPS
6. Add reverse proxy (nginx)
7. Use docker secrets for passwords

## Clean Slate

To start fresh:
```bash
# Stop and remove everything
docker-compose down -v

# Remove all images
docker-compose down --rmi all

# Rebuild from scratch
docker-compose up --build
```

## Performance Tips

- **First build**: Takes 5-10 minutes (downloading images, npm install)
- **Subsequent builds**: ~1-2 minutes (uses cache)
- **Hot reload**: Backend changes reflect immediately
- **Frontend changes**: Requires rebuild (`docker-compose up --build frontend`)

## What's Different?

**Previous setup**: Used old `frontend/` directory  
**New setup**: Uses `newfront_end/` directory with:
- ✅ Advent of Code UI
- ✅ Puzzle calendar
- ✅ 1v1 matches
- ✅ Real-time WebSocket
- ✅ Leaderboards

---

**Now when you run `docker-compose up`, you get the new puzzle platform!** 🎉
