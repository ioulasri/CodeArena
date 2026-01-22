# CodeArena

A full-stack web application built with FastAPI and React.js.

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

### Using Docker (Recommended)

```bash
# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Local Development

See [docs/setup-guide.md](docs/setup-guide.md) for detailed setup instructions.

## Technologies

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: React.js, React Router, Axios
- **DevOps**: Docker, Docker Compose, Nginx

## Documentation

- [Architecture Overview](docs/architecture.md)
- [Database Schema](docs/database-schema.md)
- [Setup Guide](docs/setup-guide.md)

## Development

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## Testing

```bash
# Backend tests
cd backend && pytest

# Frontend tests
cd frontend && npm test
```

## License

TBD

## Contributing

TBD
