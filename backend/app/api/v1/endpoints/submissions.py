from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.submission import Submission
from app.schemas.submission import SubmissionResponse, SubmissionCreate

router = APIRouter()

@router.post("/", response_model=SubmissionResponse, status_code=status.HTTP_201_CREATED)
async def create_submission(
    submission_data: SubmissionCreate,
    db: Session = Depends(get_db)
):
    """Submit code for a problem"""
    # TODO: Add authentication to get current user
    # TODO: Implement code execution service in Week 3
    
    db_submission = Submission(
        **submission_data.dict(),
        status="PENDING"
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    
    return db_submission

@router.get("/{submission_id}", response_model=SubmissionResponse)
async def get_submission(submission_id: int, db: Session = Depends(get_db)):
    """Get submission by ID"""
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )
    
    return submission

@router.get("/user/{user_id}", response_model=List[SubmissionResponse])
async def get_user_submissions(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get all submissions for a user"""
    submissions = db.query(Submission).filter(
        Submission.user_id == user_id
    ).offset(skip).limit(limit).all()
    
    return submissions

@router.get("/problem/{problem_id}", response_model=List[SubmissionResponse])
async def get_problem_submissions(
    problem_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get all submissions for a problem"""
    submissions = db.query(Submission).filter(
        Submission.problem_id == problem_id
    ).offset(skip).limit(limit).all()
    
    return submissions
