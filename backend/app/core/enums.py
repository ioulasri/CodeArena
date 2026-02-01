"""
Enums for CodeArena
Provides type-safe constants for status values and other magic strings
"""

from enum import Enum


class MatchStatus(str, Enum):
    """Match status values"""
    WAITING = "waiting"
    READY = "ready"
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class PuzzleDifficulty(str, Enum):
    """Puzzle difficulty levels"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class WebSocketMessageType(str, Enum):
    """WebSocket message types"""
    PING = "ping"
    PONG = "pong"
    PLAYER_CONNECTED = "player_connected"
    PLAYER_DISCONNECTED = "player_disconnected"
    PLAYER_READY = "player_ready"
    MATCH_STARTED = "match_started"
    ANSWER_SUBMITTED = "answer_submitted"
    MATCH_COMPLETED = "match_completed"
