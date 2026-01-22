from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.problem import Problem
from app.schemas.problem import ProblemResponse, ProblemCreate

router = APIRouter()

@router.get("/", response_model=List[ProblemResponse])
async def list_problems(
    skip: int = 0,
    limit: int = 10,
    difficulty: Optional[str] = Query(None, description="Filter by difficulty: EASY, MEDIUM, HARD"),
    category: Optional[str] = Query(None, description="Filter by category"),
    db: Session = Depends(get_db)
):
    """List all problems with optional filters"""
    query = db.query(Problem)
    
    if difficulty:
        query = query.filter(Problem.difficulty == difficulty)
    
    if category:
        query = query.filter(Problem.category == category)
    
    problems = query.offset(skip).limit(limit).all()
    return problems

@router.get("/{problem_id}", response_model=ProblemResponse)
async def get_problem(problem_id: int, db: Session = Depends(get_db)):
    """Get problem by ID"""
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found"
        )
    
    return problem

@router.get("/slug/{slug}", response_model=ProblemResponse)
async def get_problem_by_slug(slug: str, db: Session = Depends(get_db)):
    """Get problem by slug"""
    problem = db.query(Problem).filter(Problem.slug == slug).first()
    
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found"
        )
    
    return problem

@router.post("/", response_model=ProblemResponse, status_code=status.HTTP_201_CREATED)
async def create_problem(
    problem_data: ProblemCreate,
    db: Session = Depends(get_db)
):
    """Create a new problem (admin only - to be implemented)"""
    # TODO: Add admin authentication check
    db_problem = Problem(**problem_data.dict())
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    
    return db_problem
