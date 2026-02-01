"""
Puzzle and Match Models
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, Float, CheckConstraint, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Puzzle(Base):
    __tablename__ = "puzzles"

    id = Column(Integer, primary_key=True, index=True)
    day = Column(Integer, unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    story = Column(Text)
    sample_input = Column(Text)
    sample_output = Column(Text)
    difficulty = Column(String(20), default='medium')
    generator_type = Column(String(50), nullable=False)
    generator_params = Column(JSONB, default={})
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    matches = relationship("Match", back_populates="puzzle")


class Match(Base):
    __tablename__ = "matches"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    puzzle_id = Column(Integer, ForeignKey('puzzles.id', ondelete='CASCADE'))
    player1_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    player2_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    status = Column(String(20), default='waiting')  # waiting, ready, active, completed, abandoned
    winner_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    room_code = Column(String(10), unique=True, nullable=True)
    started_at = Column(TIMESTAMP, nullable=True)
    completed_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    __table_args__ = (
        CheckConstraint('player1_id != player2_id', name='different_players'),
    )
    
    # Relationships
    puzzle = relationship("Puzzle", back_populates="matches")
    player1 = relationship("User", foreign_keys=[player1_id])
    player2 = relationship("User", foreign_keys=[player2_id])
    winner = relationship("User", foreign_keys=[winner_id])
    player_inputs = relationship("PlayerPuzzleInput", back_populates="match", cascade="all, delete-orphan")
    player_answers = relationship("PlayerAnswer", back_populates="match", cascade="all, delete-orphan")


class PlayerPuzzleInput(Base):
    __tablename__ = "player_puzzle_inputs"
    
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(UUID(as_uuid=True), ForeignKey('matches.id', ondelete='CASCADE'))
    player_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    puzzle_id = Column(Integer, ForeignKey('puzzles.id', ondelete='CASCADE'))
    input_data = Column(Text, nullable=False)
    expected_answer = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    # Relationships
    match = relationship("Match", back_populates="player_inputs")
    player = relationship("User")
    puzzle = relationship("Puzzle")


class PlayerAnswer(Base):
    __tablename__ = "player_answers"
    
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(UUID(as_uuid=True), ForeignKey('matches.id', ondelete='CASCADE'))
    player_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    puzzle_id = Column(Integer, ForeignKey('puzzles.id', ondelete='CASCADE'))
    submitted_answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    submitted_at = Column(TIMESTAMP, default=datetime.utcnow)
    time_taken_seconds = Column(Integer)
    
    # Relationships
    match = relationship("Match", back_populates="player_answers")
    player = relationship("User")
    puzzle = relationship("Puzzle")


class MatchStats(Base):
    __tablename__ = "match_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    total_matches = Column(Integer, default=0)
    matches_won = Column(Integer, default=0)
    matches_lost = Column(Integer, default=0)
    total_puzzles_solved = Column(Integer, default=0)
    fastest_solve_seconds = Column(Integer, nullable=True)
    average_solve_seconds = Column(Float, nullable=True)
    current_streak = Column(Integer, default=0)
    best_streak = Column(Integer, default=0)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
