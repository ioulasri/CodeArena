# CodeArena Quick Reference Card 🚀

> **Keep this handy while developing!**

## Emergency Commands

```bash
# Something broken? Start here:
docker-compose down && docker-compose up -d
docker-compose logs -f

# Nuclear option (deletes everything, starts fresh):
docker-compose down -v
docker-compose up -d
docker-compose exec backend python backend/scripts/seed_data.py
```

## Daily Development Commands

```bash
# Start working
docker-compose up -d
docker-compose logs -f backend frontend

# Make backend changes
# Just edit files - changes auto-reload! ✨

# Make frontend changes
docker-compose build frontend
docker-compose up -d frontend

# Check what's running
docker-compose ps

# Stop working
docker-compose down
```

## Common Tasks (Copy-Paste Ready!)

### Add a New API Endpoint

**Backend:**
```python
# backend/app/routers/YOUR_ROUTER.py
@router.get("/your-endpoint")
async def your_function(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # If auth needed
):
    return {"message": "Hello!"}
```

**Frontend:**
```javascript
// frontend/src/components/Terminal.js
const fetchData = async () => {
    const response = await fetch(`${API_URL}/api/v1/your-endpoint`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await response.json();
    console.log(data);
};
```

### Add a Database Column

```python
# 1. Edit model
class Problem(Base):
    new_field = Column(String)  # Add this

# 2. Terminal:
docker-compose exec backend alembic revision --autogenerate -m "add new field"
docker-compose exec backend alembic upgrade head
```

### Change Network IP

```yaml
# docker-compose.yml
frontend:
  build:
    args:
      REACT_APP_API_URL: http://YOUR_NEW_IP:8000

# backend/app/main.py
allow_origins=["http://YOUR_NEW_IP:3000"]
```

```bash
# Rebuild
docker-compose build frontend
docker-compose restart backend
docker-compose up -d frontend
```

### Add a New Problem (SQL)

```sql
docker-compose exec postgres psql -U postgres codearena

INSERT INTO problems (title, description, difficulty, category, created_at)
VALUES (
    'Your Problem Title',
    'Problem description here',
    'Easy',
    'Arrays',
    NOW()
);
```

### Check Logs for Errors

```bash
# Backend errors
docker-compose logs backend | grep -i error

# Frontend build errors
docker-compose logs frontend

# Database errors
docker-compose logs postgres
```

## File Structure (Where to Look)

```
CodeArena/
├── backend/
│   └── app/
│       ├── main.py          ← CORS, startup
│       ├── routers/         ← API endpoints HERE
│       ├── models/          ← Database tables HERE
│       ├── schemas/         ← Data validation HERE
│       └── services/        ← Business logic HERE
├── frontend/
│   └── src/
│       ├── App.js           ← Auth logic HERE
│       └── components/      ← UI components HERE
├── docker-compose.yml       ← Services config HERE
└── docker/
    ├── backend.dockerfile   ← Backend build HERE
    └── frontend.dockerfile  ← Frontend build HERE
```

## Debugging Checklist

**API not working?**
```bash
# 1. Is backend running?
docker-compose ps backend

# 2. Check backend logs
docker-compose logs backend --tail=50

# 3. Test API directly
curl http://localhost:8000/api/v1/problems/

# 4. Check CORS
curl -H "Origin: http://localhost:3000" http://localhost:8000/api/v1/problems/ -v
```

**Frontend not updating?**
```bash
# 1. Did you rebuild?
docker-compose build frontend
docker-compose up -d frontend

# 2. Clear browser cache
# Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows/Linux)

# 3. Check what's in the build
docker-compose exec frontend sh -c "cat /usr/share/nginx/html/static/js/main.*.js | grep 'YOUR_CHANGE'"
```

**Database issues?**
```bash
# 1. Is it running?
docker-compose ps postgres

# 2. Connect to it
docker-compose exec postgres psql -U postgres codearena

# 3. Check tables
\dt

# 4. Query data
SELECT * FROM users;
```

**Code execution not working?**
```bash
# 1. Is Docker socket mounted?
docker-compose exec backend ls -la /var/run/docker.sock

# 2. Check execution logs
docker-compose logs backend | grep -i "code execution"

# 3. Test manually
docker run --rm python:3.11-slim python -c "print('Hello')"
```

## Port Reference

| Service | Port | Access From |
|---------|------|-------------|
| Frontend | 3000 | http://localhost:3000 |
| Backend | 8000 | http://localhost:8000 |
| Backend Docs | 8000 | http://localhost:8000/docs |
| Database | 5432 | localhost:5432 |

## Environment Variables

**Frontend (Build-time!):**
```env
REACT_APP_API_URL=http://192.168.100.2:8000
```
⚠️ **Must rebuild after changing!**

**Backend (Runtime):**
```env
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/codearena
SECRET_KEY=your-secret-key
```
✅ **Just restart after changing**

## Git Workflow

```bash
# 1. Create branch
git checkout -b feature/my-feature

# 2. Make changes

# 3. Commit
git add .
git commit -m "feat: add my feature"

# 4. Push
git push -u origin feature/my-feature

# 5. Create PR on GitHub

# 6. Merge, then:
git checkout main
git pull
git branch -d feature/my-feature
```

## API Testing with curl

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@test.com","password":"test123"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Get problems (with auth)
curl http://localhost:8000/api/v1/problems/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Common Error Messages & Fixes

| Error | Fix |
|-------|-----|
| `Cannot connect to Docker daemon` | Start Docker Desktop |
| `Port already in use` | `lsof -i :PORT` then `kill -9 PID` |
| `502 Bad Gateway` | Backend not ready, check logs |
| `Module not found` | `docker-compose build backend` |
| `relation does not exist` | Run migrations or seed data |
| `CORS error` | Add origin to `allow_origins` in main.py |

## Performance Tips

```python
# Add database indexes
class Problem(Base):
    __table_args__ = (Index('idx_difficulty', 'difficulty'),)

# Cache expensive queries
from functools import lru_cache
@lru_cache(maxsize=100)
def expensive_function():
    pass

# Use async properly
async def fetch_data():
    await db.query(...)  # Don't forget await!
```

## Security Checklist

- [ ] Environment variables not committed (check .env files)
- [ ] Strong SECRET_KEY (not 'dev-secret-key...')
- [ ] CORS configured for production domain
- [ ] Database password changed from defaults
- [ ] User input validated (Pydantic schemas)
- [ ] SQL injection prevented (SQLAlchemy, no raw SQL)
- [ ] Code execution limits (memory, CPU, timeout)

## When to Rebuild vs Restart

**Rebuild (slow):**
- ✅ Changed Dockerfile
- ✅ Changed requirements.txt / package.json
- ✅ Changed frontend code (production)
- ❌ Changed Python code (auto-reloads)

**Restart (fast):**
- ✅ Changed environment variables
- ✅ Changed configuration
- ✅ After database migrations

**Neither (instant):**
- ✅ Python code changes (volume-mounted)
- ✅ React in dev mode (`npm start`)

## Help Resources

| Topic | Resource |
|-------|----------|
| FastAPI | https://fastapi.tiangolo.com |
| React | https://react.dev/learn |
| Docker | https://docs.docker.com |
| PostgreSQL | https://www.postgresql.org/docs |
| SQLAlchemy | https://docs.sqlalchemy.org |

## Your Turn! ✨

**Easy wins to start:**
1. Change the welcome message in Terminal.js
2. Add a new problem via SQL
3. Change the terminal color scheme in CSS
4. Add a "Copy Code" button

**Ready for more:**
1. Add a user profile page
2. Add problem categories filter
3. Add submission statistics
4. Add code syntax highlighting

---

**Pro Tip:** Keep this file open in a tab while coding!

**Remember:** 
- 🔍 Check logs when stuck
- 🧪 Use the debug page (http://localhost:3000/debug.html)
- 📖 Refer to DEVELOPMENT_GUIDE.md for deep dives
- 💡 Google error messages
- 🎯 Start small, iterate fast

**You've got this! Happy coding! 🚀**
