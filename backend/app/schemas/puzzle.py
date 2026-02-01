"""
Pydantic schemas for Puzzle and Match APIs
"""

from pydantic import BaseModel, UUID4
from typing import Optional, Dict, Any
from datetime import datetime


# Puzzle Schemas
class PuzzleBase(BaseModel):
    day: int
    title: str
    description: str
    story: Optional[str] = None
    sample_input: Optional[str] = None
    sample_output: Optional[str] = None
    difficulty: str = 'medium'
    generator_type: str
    generator_params: Dict[str, Any] = {}


class PuzzleCreate(PuzzleBase):
    pass


class PuzzleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    story: Optional[str] = None
    sample_input: Optional[str] = None
    sample_output: Optional[str] = None
    difficulty: Optional[str] = None
    is_active: Optional[bool] = None


class PuzzleResponse(BaseModel):
    id: int
    day: int
    title: str
    description: str
    story: Optional[str] = None
    sample_input: Optional[str] = None
    sample_output: Optional[str] = None
    difficulty: str
    generator_type: str
    generator_params: Optional[Dict[str, Any]] = None
    is_active: bool
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Match Schemas
class MatchCreate(BaseModel):
    puzzle_id: int
    room_code: Optional[str] = None  # For private matches


class MatchJoin(BaseModel):
    room_code: Optional[str] = None  # Join by room code or auto-match


class MatchResponse(BaseModel):
    id: UUID4
    puzzle_id: int
    player1_id: Optional[int] = None
    player2_id: Optional[int] = None
    status: str
    winner_id: Optional[int] = None
    room_code: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class MatchDetailResponse(MatchResponse):
    puzzle: PuzzleResponse
    player1_username: Optional[str] = None
    player2_username: Optional[str] = None
    winner_username: Optional[str] = None


# Player Input Schema
class PlayerInputResponse(BaseModel):
    input_data: str
    puzzle_id: int
    puzzle_title: str
    puzzle_description: str
    puzzle_story: Optional[str] = None
    
    class Config:
        from_attributes = True


# Answer Submission Schema
class AnswerSubmit(BaseModel):
    answer: str


class AnswerResponse(BaseModel):
    is_correct: bool
    match_status: str
    winner_id: Optional[int] = None
    time_taken_seconds: Optional[int] = None
    message: str


# Match Stats Schema
class MatchStatsResponse(BaseModel):
    user_id: int
    username: str
    total_matches: int
    matches_won: int
    matches_lost: int
    win_rate: float
    total_puzzles_solved: int
    fastest_solve_seconds: Optional[int] = None
    average_solve_seconds: Optional[float] = None
    current_streak: int
    best_streak: int
    
    class Config:
        from_attributes = True


# Leaderboard Schema
class LeaderboardEntry(BaseModel):
    id: int
    username: str
    total_matches: int
    matches_won: int
    matches_lost: int
    win_rate: float
    total_puzzles_solved: int
    fastest_solve_seconds: Optional[int] = None
    average_solve_seconds: Optional[float] = None
    current_streak: Optional[int] = 0
    best_streak: Optional[int] = 0


# Match History Schema
class MatchHistoryEntry(BaseModel):
    id: UUID4
    puzzle_day: int
    puzzle_title: str
    opponent_username: str
    won: bool
    time_taken_seconds: Optional[int] = None
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
