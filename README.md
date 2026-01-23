# CodeArena

A competitive programming platform with a terminal-style interface for solving coding challenges. Features Docker-based code execution, multi-language support, and real-time submission evaluation.

## ✨ Features

- 🖥️ **Terminal-Style UI** - Black screen with green text for the authentic hacker experience
- 🔐 **Authentication System** - Secure user registration and login with JWT tokens
- 📝 **Problem Browser** - Browse and solve coding challenges by difficulty and category
- 💻 **Multi-Language Support** - Python, JavaScript, Java, and C++
- 🐳 **Sandboxed Execution** - Safe code execution in isolated Docker containers
- ⚡ **Real-Time Evaluation** - Instant feedback with test case validation
- 📊 **Submission History** - Track your progress and previous attempts

## Project Structure

```
codearena/
├── backend/                 # FastAPI application
│   ├── app/                # Application code
│   ├── tests/              # Backend tests
│   ├── .env.example        # Environment variables template
│   ├── requirements.txt    # Python dependencies
│   └── README.md           # Backend documentation
├── frontend/                # React.js application
│   ├── public/             # Static files
│   ├── src/                # React components
│   ├── .env.example        # Environment variables template
│   ├── package.json        # Node dependencies
│   └── README.md           # Frontend documentation
├── docker/                  # Docker configurations
│   ├── backend.dockerfile  # Backend container
│   ├── frontend.dockerfile # Frontend container
│   └── nginx.conf          # Nginx configuration
├── docs/                    # Documentation
│   ├── architecture.md     # System architecture
│   ├── database-schema.md  # Database design
│   └── setup-guide.md      # Setup instructions
├── docker-compose.yml       # Local development orchestration
└── README.md                # This file
```

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Git

### 🚀 Running with Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/ioulasri/CodeArena.git
   cd CodeArena
   ```

2. **Start all services**
   ```bash
   docker-compose up -d
   ```

   This will start:
   - PostgreSQL database on port 5432
   - FastAPI backend on port 8000
   - React frontend (via Nginx) on port 3000

3. **Seed the database with sample problems**
   ```bash
   docker-compose exec backend python -m scripts.seed_data
   ```

   This creates:
   - Admin user (username: `admin`, password: `admin123`)
   - 4 sample problems (Two Sum, Reverse String, Fizz Buzz, Palindrome Number)

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

5. **Login and start coding!**
   - Use the credentials: `admin` / `admin123`
   - Browse problems in the terminal interface
   - Write and submit your solutions

### 🛠️ Managing Services

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart a specific service
docker-compose restart backend
docker-compose restart frontend

# Rebuild after code changes
docker-compose up -d --build
```

### Local Development

For development without Docker:

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database URL

# Run migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env

# Start the development server
npm start
```

#### Database Setup
```bash
# Using Docker for PostgreSQL only
docker run -d \
  --name codearena-db \
  -e POSTGRES_DB=codearena \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  postgres:15-alpine
```

## Technologies

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Docker SDK
- **Frontend**: React 18, Terminal-style CSS
- **Code Execution**: Docker containers with Python 3.11, Node 18, OpenJDK 17, GCC 12
- **DevOps**: Docker, Docker Compose, Nginx
- **Authentication**: JWT tokens with bcrypt password hashing

## Documentation

- [Architecture Story](docs/architecture-story.md) - Comprehensive system design explained as a narrative
- [Database Schema](docs/database-schema.md) - Database tables and relationships
- [Setup Guide](docs/setup-guide.md) - Detailed setup instructions

## 🏗️ Architecture

### Code Execution Flow

1. **User submits code** via the terminal interface
2. **Backend receives submission** and stores it in PostgreSQL
3. **Background task** queues the evaluation
4. **CodeExecutor service** creates an isolated Docker container
5. **Code runs** with test inputs in the sandboxed environment
6. **SubmissionEvaluator** compares outputs with expected results
7. **Verdict is determined** (ACCEPTED, WRONG_ANSWER, TIME_LIMIT_EXCEEDED, etc.)
8. **Database is updated** with results and execution metrics
9. **User sees results** in real-time on the terminal interface

### Security Features

- Network disabled in code execution containers
- All Linux capabilities dropped
- No new privileges flag set
- Temporary file isolation
- Resource limits (CPU, memory, time)
- User authentication with JWT tokens

## Environment Variables

### Backend (.env)
```bash
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/codearena
SECRET_KEY=your-secret-key-here
API_HOST=0.0.0.0
API_PORT=8000
```

### Frontend (.env)
```bash
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000/ws
REACT_APP_ENVIRONMENT=development
```

## Development

### Backend Development
```bash
cd backend

# Activate virtual environment
source venv/bin/activate

# Run with auto-reload
uvicorn app.main:app --reload

# Run tests
pytest

# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

### Frontend Development
```bash
cd frontend

# Start development server
npm start

# Run tests
npm test

# Build for production
npm run build

# Lint code
npm run lint
```

### Adding New Problems

```bash
# Connect to backend container
docker-compose exec backend python

# In Python shell:
from app.database import SessionLocal
from app.models import Problem

db = SessionLocal()
problem = Problem(
    title="Your Problem Title",
    slug="your-problem-slug",
    description="Problem description...",
    difficulty="EASY",  # or MEDIUM, HARD
    category="Arrays",
    # Add test cases...
)
db.add(problem)
db.commit()
```

## Testing

### Backend Tests
```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

### Frontend Tests
```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch
```

### End-to-End Testing

1. Start all services: `docker-compose up -d`
2. Seed database: `docker-compose exec backend python -m scripts.seed_data`
3. Navigate to http://localhost:3000
4. Login with `admin` / `admin123`
5. Select "Two Sum" problem
6. Submit a solution and verify execution

## 🐛 Troubleshooting

### Docker Issues

**Containers won't start:**
```bash
docker-compose down
docker-compose up -d --build
```

**Database connection errors:**
```bash
# Check if PostgreSQL is healthy
docker-compose ps

# View database logs
docker-compose logs postgres
```

**Frontend not loading:**
```bash
# Rebuild frontend container
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

### Code Execution Issues

**Submissions stuck in PENDING:**
- Check backend logs: `docker-compose logs backend`
- Verify Docker socket is accessible
- Ensure Docker SDK is installed: `pip install docker==7.0.0`

**Language not supported:**
- Check available Docker images
- Verify language configuration in `code_executor.py`

## 📦 Project Structure Details

```
codearena/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/    # API routes
│   │   ├── core/                # Configuration & security
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── services/            # Business logic
│   │   │   ├── code_executor.py       # Docker-based execution
│   │   │   └── submission_evaluator.py # Test case checking
│   │   └── main.py              # FastAPI app
│   ├── scripts/
│   │   └── seed_data.py         # Database seeding
│   └── tests/                   # Backend tests
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Login.js         # Authentication UI
│   │   │   ├── Terminal.js      # Main terminal interface
│   │   │   └── *.css            # Terminal styling
│   │   ├── App.js               # Root component
│   │   └── index.js             # Entry point
│   └── public/                  # Static assets
├── docker/
│   ├── backend.dockerfile       # Backend container config
│   ├── frontend.dockerfile      # Multi-stage React build
│   └── nginx.conf               # Nginx server config
└── docs/
    └── architecture-story.md    # System design narrative
```

## 🚧 Roadmap

- [ ] WebSocket support for real-time updates
- [ ] Contest system with timed challenges
- [ ] Leaderboard and rankings
- [ ] More programming languages (Rust, Go, Ruby)
- [ ] Code editor with syntax highlighting
- [ ] Problem difficulty ratings
- [ ] User profiles and statistics
- [ ] Problem tags and filtering
- [ ] Solution discussions and comments
- [ ] Admin dashboard for problem management

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

### Commit Convention

- `feat:` New feature
- `fix:` Bug fix
- `refactor:` Code refactoring
- `docs:` Documentation changes
- `chore:` Maintenance tasks
- `test:` Test additions or changes

## 📄 License

MIT License - feel free to use this project for learning and development purposes.

## 👥 Authors

- **Imad Oulasri** ([@ioulasri](https://github.com/ioulasri)) - Creator & Lead Developer

## 🙏 Acknowledgments

- FastAPI for the amazing web framework
- React for the frontend library
- Docker for containerization
- PostgreSQL for reliable data storage
