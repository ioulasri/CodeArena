"""
Admin API Endpoints
File: app/api/v1/endpoints/admin.py
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List
from datetime import datetime, timedelta

from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user_dependency as get_current_user
from app.models.user import User
from app.models.puzzle import Puzzle, Match, MatchStats, PlayerAnswer
from app.schemas.admin import (
    PuzzleCreate, PuzzleUpdate, UserUpdate, UserStats,
    SystemStats, MatchDetails
)
from app.schemas.puzzle import PuzzleResponse

router = APIRouter()


# Admin authorization dependency
def get_admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


# ============= PUZZLE MANAGEMENT =============

@router.post("/puzzles", response_model=PuzzleResponse, status_code=status.HTTP_201_CREATED)
async def create_puzzle(
    puzzle_data: PuzzleCreate,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new puzzle"""
    # Check if day already exists
    existing = db.query(Puzzle).filter(Puzzle.day == puzzle_data.day).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Puzzle for day {puzzle_data.day} already exists"
        )
    
    puzzle = Puzzle(**puzzle_data.dict())
    db.add(puzzle)
    db.commit()
    db.refresh(puzzle)
    return puzzle


@router.put("/puzzles/{puzzle_id}", response_model=PuzzleResponse)
async def update_puzzle(
    puzzle_id: int,
    puzzle_data: PuzzleUpdate,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Update an existing puzzle"""
    puzzle = db.query(Puzzle).filter(Puzzle.id == puzzle_id).first()
    if not puzzle:
        raise HTTPException(status_code=404, detail="Puzzle not found")
    
    update_data = puzzle_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(puzzle, field, value)
    
    puzzle.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(puzzle)
    return puzzle


@router.delete("/puzzles/{puzzle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_puzzle(
    puzzle_id: int,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Delete a puzzle"""
    puzzle = db.query(Puzzle).filter(Puzzle.id == puzzle_id).first()
    if not puzzle:
        raise HTTPException(status_code=404, detail="Puzzle not found")
    
    db.delete(puzzle)
    db.commit()
    return None


# ============= USER MANAGEMENT =============

@router.get("/users", response_model=List[UserStats])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get all users with their stats"""
    users = db.query(User).offset(skip).limit(limit).all()
    
    user_stats = []
    for user in users:
        stats = db.query(MatchStats).filter(MatchStats.user_id == user.id).first()
        
        win_rate = 0.0
        if stats and stats.total_matches > 0:
            win_rate = round((stats.matches_won / stats.total_matches) * 100, 2)
        
        user_stats.append(UserStats(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            is_admin=user.is_admin,
            created_at=user.created_at,
            total_matches=stats.total_matches if stats else 0,
            matches_won=stats.matches_won if stats else 0,
            matches_lost=stats.matches_lost if stats else 0,
            win_rate=win_rate
        ))
    
    return user_stats


@router.put("/users/{user_id}")
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Update user (ban/unban, grant/revoke admin)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    user.updated_at = datetime.now()
    db.commit()
    db.refresh(user)
    
    return {
        "id": user.id,
        "username": user.username,
        "is_active": user.is_active,
        "is_admin": user.is_admin
    }


# ============= ANALYTICS & MONITORING =============

@router.get("/stats/system", response_model=SystemStats)
async def get_system_stats(
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get overall system statistics"""
    
    # User stats
    total_users = db.query(func.count(User.id)).scalar()
    active_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar()
    
    # Puzzle stats
    total_puzzles = db.query(func.count(Puzzle.id)).scalar()
    active_puzzles = db.query(func.count(Puzzle.id)).filter(Puzzle.is_active == True).scalar()
    
    # Match stats
    total_matches = db.query(func.count(Match.id)).scalar()
    active_matches = db.query(func.count(Match.id)).filter(
        Match.status.in_(['waiting', 'ready', 'active'])
    ).scalar()
    
    # Matches today
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    matches_today = db.query(func.count(Match.id)).filter(
        Match.created_at >= today_start
    ).scalar()
    
    # Matches this week
    week_start = today_start - timedelta(days=today_start.weekday())
    matches_this_week = db.query(func.count(Match.id)).filter(
        Match.created_at >= week_start
    ).scalar()
    
    # Average match duration
    completed_matches = db.query(Match).filter(
        and_(Match.completed_at.isnot(None), Match.started_at.isnot(None))
    ).all()
    
    avg_duration = None
    if completed_matches:
        durations = [
            (m.completed_at - m.started_at).total_seconds() 
            for m in completed_matches
        ]
        avg_duration = sum(durations) / len(durations)
    
    return SystemStats(
        total_users=total_users,
        active_users=active_users,
        total_puzzles=total_puzzles,
        active_puzzles=active_puzzles,
        total_matches=total_matches,
        active_matches=active_matches,
        matches_today=matches_today,
        matches_this_week=matches_this_week,
        avg_match_duration_seconds=avg_duration
    )


@router.get("/matches/recent", response_model=List[MatchDetails])
async def get_recent_matches(
    limit: int = 50,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get recent matches with details"""
    matches = db.query(Match).order_by(Match.created_at.desc()).limit(limit).all()
    
    match_details = []
    for match in matches:
        puzzle = db.query(Puzzle).filter(Puzzle.id == match.puzzle_id).first()
        player1 = db.query(User).filter(User.id == match.player1_id).first()
        player2 = db.query(User).filter(User.id == match.player2_id).first() if match.player2_id else None
        winner = db.query(User).filter(User.id == match.winner_id).first() if match.winner_id else None
        
        duration = None
        if match.started_at and match.completed_at:
            duration = int((match.completed_at - match.started_at).total_seconds())
        
        match_details.append(MatchDetails(
            match_id=str(match.id),
            puzzle_day=puzzle.day if puzzle else 0,
            puzzle_title=puzzle.title if puzzle else "Unknown",
            player1_username=player1.username if player1 else "Unknown",
            player2_username=player2.username if player2 else None,
            status=match.status,
            winner_username=winner.username if winner else None,
            started_at=match.started_at,
            completed_at=match.completed_at,
            duration_seconds=duration
        ))
    
    return match_details


@router.get("/matches/active", response_model=List[MatchDetails])
async def get_active_matches(
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get all currently active matches"""
    matches = db.query(Match).filter(
        Match.status.in_(['waiting', 'ready', 'active'])
    ).order_by(Match.created_at.desc()).all()
    
    match_details = []
    for match in matches:
        puzzle = db.query(Puzzle).filter(Puzzle.id == match.puzzle_id).first()
        player1 = db.query(User).filter(User.id == match.player1_id).first()
        player2 = db.query(User).filter(User.id == match.player2_id).first() if match.player2_id else None
        
        match_details.append(MatchDetails(
            match_id=str(match.id),
            puzzle_day=puzzle.day if puzzle else 0,
            puzzle_title=puzzle.title if puzzle else "Unknown",
            player1_username=player1.username if player1 else "Unknown",
            player2_username=player2.username if player2 else None,
            status=match.status,
            winner_username=None,
            started_at=match.started_at,
            completed_at=None,
            duration_seconds=None
        ))
    
    return match_details