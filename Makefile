.PHONY: help up down logs restart clean db-migrate db-reset backend-install backend-run backend-test frontend-install frontend-run frontend-build

# Default target
help:
	@echo "CodeArena Development Commands"
	@echo "=============================="
	@echo ""
	@echo "Docker Commands:"
	@echo "  make up              - Start all services (postgres, backend)"
	@echo "  make down            - Stop all services"
	@echo "  make logs            - Show logs from all services"
	@echo "  make restart         - Restart all services"
	@echo "  make clean           - Remove all containers and volumes"
	@echo ""
	@echo "Database Commands:"
	@echo "  make db-migrate      - Run database migrations"
	@echo "  make db-reset        - Drop and recreate database"
	@echo "  make db-shell        - Open PostgreSQL shell"
	@echo ""
	@echo "Backend Commands:"
	@echo "  make backend-install - Install backend dependencies"
	@echo "  make backend-run     - Run backend locally"
	@echo "  make backend-test    - Run backend tests"
	@echo "  make backend-shell   - Activate backend virtual environment"
	@echo ""
	@echo "Frontend Commands:"
	@echo "  make frontend-install - Install frontend dependencies"
	@echo "  make frontend-run     - Run frontend dev server"
	@echo "  make frontend-build   - Build frontend for production"
	@echo ""

# Docker Commands
up:
	docker-compose up -d postgres backend frontend

down:
	docker-compose down

build:
	docker-compose build

logs:
	docker-compose logs -f

restart:
	docker-compose restart

clean:
	docker-compose down -v
	rm -rf backend/venv newfront_end/node_modules

# Database Commands
db-migrate:
	docker exec -i codearena-db psql -U postgres -d codearena < backend/migrations/001_initial_schema.sql
	docker exec -i codearena-db psql -U postgres -d codearena < backend/migrations/002_puzzle_match_schema.sql

db-seed:
	# Seed sample puzzles for local testing
	docker exec -i codearena-db psql -U postgres -d codearena < backend/migrations/007_seed_puzzles.sql

db-reset:
	docker exec -i codearena-db psql -U postgres -c "DROP DATABASE IF EXISTS codearena;"
	docker exec -i codearena-db psql -U postgres -c "CREATE DATABASE codearena;"
	$(MAKE) db-migrate

db-shell:
	docker exec -it codearena-db psql -U postgres -d codearena

# Backend Commands
backend-install:
	cd backend && /usr/local/bin/python3.10 -m venv venv && \
	. venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements.txt

backend-run:
	cd backend && . venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

backend-test:
	cd backend && . venv/bin/activate && pytest

backend-shell:
	@echo "Run: cd backend && source venv/bin/activate"

# Frontend Commands
frontend-install:
	cd newfront_end && npm install

frontend-run:
	cd newfront_end && npm start

frontend-build:
	cd newfront_end && npm run build
