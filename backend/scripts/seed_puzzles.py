#!/usr/bin/env python3
"""
Seed the database with sample puzzles
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.puzzle import Puzzle
from app.services.puzzle_generators import PuzzleGeneratorFactory
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/codearena")

async def seed_puzzles():
    """Create sample puzzles for days 1-25"""
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    puzzle_types = ['crystal_sum', 'pattern_counter', 'grid_path', 'sequence_finder', 'tower_blocks']
    difficulties = ['easy', 'medium', 'hard']
    
    async with async_session() as session:
        # Check if puzzles already exist
        from sqlalchemy import select
        result = await session.execute(select(Puzzle))
        existing = result.scalars().all()
        
        if existing:
            print(f"⚠️  Database already has {len(existing)} puzzles. Skipping seed.")
            return
        
        print("🌱 Seeding puzzles...")
        
        puzzles_created = 0
        for day in range(1, 26):  # Days 1-25
            # Assign puzzle type (cycle through types)
            puzzle_type = puzzle_types[(day - 1) % len(puzzle_types)]
            
            # Assign difficulty (first 8 easy, next 9 medium, last 8 hard)
            if day <= 8:
                difficulty = 'easy'
            elif day <= 17:
                difficulty = 'medium'
            else:
                difficulty = 'hard'
            
            # Generate sample instance to get description
            factory = PuzzleGeneratorFactory()
            generator = factory.get_generator(puzzle_type)
            
            # Create title based on puzzle type
            titles = {
                'crystal_sum': f"Crystal Collection Day {day}",
                'pattern_counter': f"Pattern Recognition {day}",
                'grid_path': f"Maze Navigator {day}",
                'sequence_finder': f"Sequence Decoder {day}",
                'tower_blocks': f"Tower Builder {day}"
            }
            
            puzzle = Puzzle(
                day=day,
                title=titles[puzzle_type],
                description=generator.description,
                puzzle_type=puzzle_type,
                difficulty=difficulty,
                is_active=True
            )
            
            session.add(puzzle)
            puzzles_created += 1
            print(f"✅ Created: Day {day:2d} - {titles[puzzle_type]} ({difficulty})")
        
        await session.commit()
        print(f"\n🎉 Successfully seeded {puzzles_created} puzzles!")
    
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(seed_puzzles())
