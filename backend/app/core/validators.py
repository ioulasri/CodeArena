"""
Input validation utilities for CodeArena
Prevents edge cases and potential exploits
"""

import re
from typing import Optional
from fastapi import HTTPException, status


# Validation constants
MAX_USERNAME_LENGTH = 50
MIN_USERNAME_LENGTH = 3
MAX_EMAIL_LENGTH = 255
MAX_PASSWORD_LENGTH = 128
MIN_PASSWORD_LENGTH = 6
MAX_ROOM_CODE_LENGTH = 10
ROOM_CODE_PATTERN = re.compile(r'^[A-Z0-9]{6,10}$')
MAX_ANSWER_LENGTH = 10000  # Prevent abuse with gigantic answers
USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_-]+$')
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')


def validate_username(username: str) -> str:
    """Validate username format and length"""
    if not username or not username.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username cannot be empty"
        )
    
    username = username.strip()
    
    if len(username) < MIN_USERNAME_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username must be at least {MIN_USERNAME_LENGTH} characters"
        )
    
    if len(username) > MAX_USERNAME_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username cannot exceed {MAX_USERNAME_LENGTH} characters"
        )
    
    if not USERNAME_PATTERN.match(username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username can only contain letters, numbers, hyphens, and underscores"
        )
    
    return username


def validate_email(email: str) -> str:
    """Validate email format and length"""
    if not email or not email.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email cannot be empty"
        )
    
    email = email.strip().lower()
    
    if len(email) > MAX_EMAIL_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email cannot exceed {MAX_EMAIL_LENGTH} characters"
        )
    
    if not EMAIL_PATTERN.match(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )
    
    return email


def validate_password(password: str) -> str:
    """Validate password length"""
    if not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password cannot be empty"
        )
    
    if len(password) < MIN_PASSWORD_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Password must be at least {MIN_PASSWORD_LENGTH} characters"
        )
    
    if len(password) > MAX_PASSWORD_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Password cannot exceed {MAX_PASSWORD_LENGTH} characters"
        )
    
    return password


def validate_room_code(room_code: Optional[str]) -> Optional[str]:
    """Validate room code format"""
    if room_code is None:
        return None
    
    room_code = room_code.strip().upper()
    
    if not room_code:
        return None
    
    if len(room_code) > MAX_ROOM_CODE_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Room code cannot exceed {MAX_ROOM_CODE_LENGTH} characters"
        )
    
    if not ROOM_CODE_PATTERN.match(room_code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room code must contain only uppercase letters and numbers (6-10 characters)"
        )
    
    return room_code


def validate_answer(answer: str) -> str:
    """Validate answer submission"""
    if answer is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Answer cannot be empty"
        )
    
    # Normalize the answer
    answer = str(answer).strip()
    
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Answer cannot be empty"
        )
    
    if len(answer) > MAX_ANSWER_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Answer too long (max {MAX_ANSWER_LENGTH} characters)"
        )
    
    return answer


def normalize_answer(answer: str) -> str:
    """
    Normalize an answer for comparison
    Strips whitespace and converts to lowercase
    """
    return str(answer).strip().lower()
