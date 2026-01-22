from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SubmissionBase(BaseModel):
    problem_id: int
    code: str
    language: str  # python, javascript, java, cpp


class SubmissionCreate(SubmissionBase):
    user_id: int


class SubmissionResponse(SubmissionBase):
    id: int
    user_id: int
    status: str
    execution_time_ms: Optional[float] = None
    memory_used_mb: Optional[float] = None
    test_cases_passed: Optional[int] = None
    test_cases_total: Optional[int] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
