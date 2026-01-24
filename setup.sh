#!/bin/bash
# Quick setup script for CodeArena Puzzle Platform

echo "🎮 CodeArena Puzzle Platform - Setup Script"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "PUZZLE_PLATFORM_GUIDE.md" ]; then
    echo "❌ Error: Please run this script from the CodeArena root directory"
    exit 1
fi

# Backend setup
echo "📦 Setting up backend..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo "✅ Backend setup complete!"
echo ""

# Frontend setup
echo "📦 Setting up frontend..."
cd ../newfront_end

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
else
    echo "Node modules already installed!"
fi

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✅ Created .env file"
fi

echo "✅ Frontend setup complete!"
echo ""

# Database setup instructions
echo "📊 Database Setup"
echo "=================="
echo "To set up the database, run:"
echo ""
echo "1. Create database (if not exists):"
echo "   createdb codearena"
echo ""
echo "2. Run migrations:"
echo "   cd backend"
echo "   psql -U your_user -d codearena < migrations/001_initial_schema.sql"
echo "   psql -U your_user -d codearena < migrations/002_puzzle_match_schema.sql"
echo ""
echo "Replace 'your_user' with your PostgreSQL username"
echo ""

# Start instructions
echo "🚀 Starting the Platform"
echo "========================"
echo ""
echo "Terminal 1 - Start Backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "Terminal 2 - Start Frontend:"
echo "   cd newfront_end"
echo "   npm start"
echo ""
echo "Then open http://localhost:3000 in your browser!"
echo ""
echo "🎉 Setup complete! Read PUZZLE_PLATFORM_GUIDE.md for more details."
