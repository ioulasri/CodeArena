from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Boolean
from datetime import datetime
from app.core.database import Base


class Problem(Base):
    __tablename__ = "problems"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=False)
    difficulty = Column(String(20), nullable=False, index=True)  # EASY, MEDIUM, HARD
    category = Column(String(50), index=True)
    tags = Column(JSON, nullable=True)  # JSONB in PostgreSQL
    time_limit_ms = Column(Integer, default=1000)
    memory_limit_mb = Column(Integer, default=256)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)


class TestCase(Base):
    __tablename__ = "test_cases"
    
    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id", ondelete="CASCADE"), nullable=False, index=True)
    input_data = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=False)
    is_sample = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
