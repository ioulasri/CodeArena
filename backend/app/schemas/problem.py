from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ProblemBase(BaseModel):
    title: str
    slug: str
    description: str
    difficulty: str  # EASY, MEDIUM, HARD
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    time_limit_ms: int = 1000
    memory_limit_mb: int = 256


class ProblemCreate(ProblemBase):
    created_by_id: Optional[int] = None


class ProblemResponse(ProblemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
