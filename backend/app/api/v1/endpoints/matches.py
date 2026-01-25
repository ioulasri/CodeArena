"""
Puzzle and Match API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user_dependency as get_current_user
from app.models.user import User
from app.models.puzzle import Puzzle, Match
from app.schemas.puzzle import (
    PuzzleResponse, MatchCreate, MatchJoin, MatchResponse,
    AnswerSubmit, AnswerResponse, LeaderboardEntry, MatchHistoryEntry,
    MatchStatsResponse
)
from app.services.match_service import MatchService

router = APIRouter()


# Puzzle Endpoints
@router.get("/puzzles", response_model=List[PuzzleResponse])
async def get_puzzles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all active puzzles"""
    puzzles = db.query(Puzzle).filter(Puzzle.is_active == True).order_by(Puzzle.day).offset(skip).limit(limit).all()
    return puzzles


@router.get("/puzzles/{puzzle_id}", response_model=PuzzleResponse)
async def get_puzzle(
    puzzle_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific puzzle"""
    puzzle = db.query(Puzzle).filter(Puzzle.id == puzzle_id).first()
    if not puzzle:
        raise HTTPException(status_code=404, detail="Puzzle not found")
    return puzzle


# Match Endpoints
@router.post("/matches/create", response_model=MatchResponse)
async def create_match(
    match_data: MatchCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new match"""
    try:
        match = MatchService.create_match(
            db, 
            current_user.id, 
            match_data.puzzle_id, 
            match_data.room_code
        )
        return match
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/matches/join", response_model=MatchResponse)
async def join_match(
    join_data: MatchJoin,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Join an existing match"""
    try:
        match = MatchService.join_match(
            db,
            current_user.id,
            room_code=join_data.room_code
        )
        return match
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/matches/{match_id}/start")
async def start_match(
    match_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a match and get puzzle input"""
    try:
        match, player_input = MatchService.start_match(db, match_id, current_user.id)
        puzzle = db.query(Puzzle).filter(Puzzle.id == match.puzzle_id).first()

        return {
            "match_id": str(match.id),
            "status": match.status,
            "puzzle": {
                "id": puzzle.id,
                "day": puzzle.day,
                "title": puzzle.title,
                "description": puzzle.description,
                "story": puzzle.story
            },
            "input_data": player_input.get("input_data") if isinstance(player_input, dict) else player_input,
            "expected_answer": player_input.get("expected_answer") if isinstance(player_input, dict) else None,
            "started_at": match.started_at
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/matches/{match_id}/submit", response_model=AnswerResponse)
async def submit_answer(
    match_id: str,
    answer_data: AnswerSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit an answer for a match"""
    try:
        result = MatchService.submit_answer(
            db,
            match_id,
            current_user.id,
            answer_data.answer
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/matches/{match_id}")
async def get_match_details(
    match_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed match information"""
    try:
        details = MatchService.get_match_details(db, match_id, current_user.id)
        
        match = details["match"]
        puzzle = details["puzzle"]
        
        return {
            "match_id": str(match.id),
            "status": match.status,
            "puzzle": {
                "id": puzzle.id,
                "day": puzzle.day,
                "title": puzzle.title,
                "description": puzzle.description,
                "story": puzzle.story
            },
            "player1_username": details["player1_username"],
            "player2_username": details["player2_username"],
            "winner_username": details["winner_username"],
            "input_data": details["player_input"],
            "expected_answer": details["expected_answer"],
            "started_at": match.started_at,
            "completed_at": match.completed_at,
            "room_code": match.room_code
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/matches/user/history")
async def get_user_match_history(
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's match history"""
    matches = MatchService.get_user_matches(db, current_user.id, limit)
    
    history = []
    for match in matches:
        puzzle = db.query(Puzzle).filter(Puzzle.id == match.puzzle_id).first()
        
        # Determine opponent
        opponent_id = match.player2_id if match.player1_id == current_user.id else match.player1_id
        opponent = db.query(User).filter(User.id == opponent_id).first() if opponent_id else None
        
        # Check if user won
        won = match.winner_id == current_user.id
        
        # Get time taken
        from app.models.puzzle import PlayerAnswer
        answer = db.query(PlayerAnswer).filter(
            PlayerAnswer.match_id == match.id,
            PlayerAnswer.player_id == current_user.id,
            PlayerAnswer.is_correct == True
        ).first()
        
        history.append({
            "match_id": str(match.id),
            "puzzle_day": puzzle.day if puzzle else 0,
            "puzzle_title": puzzle.title if puzzle else "Unknown",
            "opponent_username": opponent.username if opponent else "Waiting...",
            "won": won,
            "status": match.status,
            "time_taken_seconds": answer.time_taken_seconds if answer else None,
            "completed_at": match.completed_at
        })
    
    return history


@router.get("/leaderboard", response_model=List[LeaderboardEntry])
async def get_leaderboard(
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get global leaderboard"""
    leaderboard = MatchService.get_leaderboard(db, limit)
    return leaderboard


@router.get("/stats/me")
async def get_my_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's statistics"""
    from app.models.puzzle import MatchStats
    
    stats = db.query(MatchStats).filter(MatchStats.user_id == current_user.id).first()
    
    if not stats:
        return {
            "user_id": current_user.id,
            "username": current_user.username,
            "total_matches": 0,
            "matches_won": 0,
            "matches_lost": 0,
            "win_rate": 0.0,
            "total_puzzles_solved": 0,
            "fastest_solve_seconds": None,
            "average_solve_seconds": None,
            "current_streak": 0,
            "best_streak": 0
        }
    
    win_rate = (stats.matches_won / stats.total_matches * 100) if stats.total_matches > 0 else 0.0
    
    return {
        "user_id": current_user.id,
        "username": current_user.username,
        "total_matches": stats.total_matches,
        "matches_won": stats.matches_won,
        "matches_lost": stats.matches_lost,
        "win_rate": round(win_rate, 2),
        "total_puzzles_solved": stats.total_puzzles_solved,
        "fastest_solve_seconds": stats.fastest_solve_seconds,
        "average_solve_seconds": round(stats.average_solve_seconds, 2) if stats.average_solve_seconds else None,
        "current_streak": stats.current_streak,
        "best_streak": stats.best_streak
    }
