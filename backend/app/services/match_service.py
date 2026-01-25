"""
Match Service - Handles match creation, joining, and management
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List, Tuple
from datetime import datetime
import random
import string

from app.models.puzzle import Match, Puzzle, PlayerPuzzleInput, PlayerAnswer, MatchStats
from app.models.user import User
from app.services.puzzle_generators import PuzzleGeneratorFactory
from app.schemas.puzzle import MatchResponse, MatchDetailResponse
from app.services.websocket_manager import manager
import asyncio
import logging
from sqlalchemy import text

logger = logging.getLogger(__name__)


class MatchService:
    """Service for managing puzzle matches"""
    
    @staticmethod
    def generate_room_code() -> str:
        """Generate a random 6-character room code"""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    @staticmethod
    def create_match(db: Session, user_id: int, puzzle_id: int, room_code: Optional[str] = None) -> Match:
        """Create a new match"""
        # Verify puzzle exists
        puzzle = db.query(Puzzle).filter(Puzzle.id == puzzle_id, Puzzle.is_active == True).first()
        if not puzzle:
            raise ValueError("Puzzle not found or not active")
        
        # Generate room code if private match
        if room_code is None:
            # Public match - try to find waiting match first
            waiting_match = db.query(Match).filter(
                Match.puzzle_id == puzzle_id,
                Match.status == 'waiting',
                Match.player2_id == None,
                Match.room_code == None,
                Match.player1_id != user_id
            ).first()
            
            if waiting_match:
                # Join existing match
                return MatchService.join_match(db, user_id, waiting_match.id)
        else:
            # Ensure room code is unique
            existing = db.query(Match).filter(Match.room_code == room_code).first()
            if existing:
                room_code = MatchService.generate_room_code()
        
        # Create new match
        match = Match(
            puzzle_id=puzzle_id,
            player1_id=user_id,
            status='waiting',
            room_code=room_code
        )
        
        db.add(match)
        db.commit()
        db.refresh(match)
        
        return match
    
    @staticmethod
    def join_match(db: Session, user_id: int, match_id: Optional[str] = None, room_code: Optional[str] = None) -> Match:
        """Join an existing match"""
        if room_code:
            match = db.query(Match).filter(Match.room_code == room_code).first()
        elif match_id:
            match = db.query(Match).filter(Match.id == match_id).first()
        else:
            # Auto-match: find any waiting public match
            match = db.query(Match).filter(
                Match.status == 'waiting',
                Match.player2_id == None,
                Match.room_code == None,
                Match.player1_id != user_id
            ).first()
        
        if not match:
            raise ValueError("No match found")
        
        if match.status != 'waiting':
            raise ValueError("Match is not accepting players")
        
        if match.player1_id == user_id:
            raise ValueError("Cannot join your own match")
        
        if match.player2_id:
            raise ValueError("Match is full")
        
        # Add second player
        match.player2_id = user_id
        match.status = 'ready'
        
        db.commit()
        db.refresh(match)
        
        return match
    
    @staticmethod
    def start_match(db: Session, match_id: str, user_id: int) -> Tuple[Match, str]:
        """
        Start a match and generate unique inputs for both players
        Returns: (match, player_input_data)
        """
        match = db.query(Match).filter(Match.id == match_id).first()
        if not match:
            raise ValueError("Match not found")
        
        # Allow start when match is 'ready' (two players),
        # or allow solo start when match is 'waiting' and no second player exists
        # and the requesting user is the match creator.
        if not (
            match.status == 'ready' or
            (match.status == 'waiting' and match.player2_id is None and user_id == match.player1_id)
        ):
            raise ValueError("Match is not ready to start")
        
        if user_id not in [match.player1_id, match.player2_id]:
            raise ValueError("You are not a player in this match")
        
        # Start the match
        match.status = 'active'
        match.started_at = datetime.utcnow()
        
        # Get puzzle
        puzzle = db.query(Puzzle).filter(Puzzle.id == match.puzzle_id).first()
        
        # Generate unique inputs for present players if not already generated
        existing_inputs = db.query(PlayerPuzzleInput).filter(
            PlayerPuzzleInput.match_id == match_id
        ).all()

        if not existing_inputs:
            player_ids = [pid for pid in (match.player1_id, match.player2_id) if pid]
            for player_id in player_ids:
                # Generate unique puzzle input
                params = puzzle.generator_params or {}
                input_data, expected_answer = PuzzleGeneratorFactory.generate_puzzle_instance(
                    puzzle.generator_type,
                    params
                )

                player_input = PlayerPuzzleInput(
                    match_id=match.id,
                    player_id=player_id,
                    puzzle_id=puzzle.id,
                    input_data=input_data,
                    expected_answer=expected_answer
                )
                db.add(player_input)
        
        db.commit()
        
        # Get this player's input
        player_input = db.query(PlayerPuzzleInput).filter(
            PlayerPuzzleInput.match_id == match_id,
            PlayerPuzzleInput.player_id == user_id
        ).first()
        # Notify any connected WebSocket clients that the match has started
        try:
            match_data = {
                "started_at": match.started_at.isoformat() if match.started_at else None,
                "puzzle": {
                    "id": puzzle.id,
                    "day": puzzle.day,
                    "title": puzzle.title,
                    "description": puzzle.description,
                    "story": puzzle.story,
                }
            }
            asyncio.create_task(manager.notify_match_start(str(match.id), match_data))
        except Exception:
            pass

        # Return match and player's input details (including expected answer)
        return match, {
            "input_data": player_input.input_data if player_input else None,
            "expected_answer": player_input.expected_answer if player_input else None
        }
    
    @staticmethod
    def submit_answer(db: Session, match_id: str, user_id: int, answer: str) -> dict:
        """Submit an answer and check if correct"""
        match = db.query(Match).filter(Match.id == match_id).first()
        if not match:
            raise ValueError("Match not found")
        
        if match.status != 'active':
            raise ValueError("Match is not active")
        
        if user_id not in [match.player1_id, match.player2_id]:
            raise ValueError("You are not a player in this match")
        
        # Get player's expected answer
        player_input = db.query(PlayerPuzzleInput).filter(
            PlayerPuzzleInput.match_id == match_id,
            PlayerPuzzleInput.player_id == user_id
        ).first()
        
        if not player_input:
            raise ValueError("No puzzle input found for player")
        
        # Check if already submitted correct answer
        correct_answer = db.query(PlayerAnswer).filter(
            PlayerAnswer.match_id == match_id,
            PlayerAnswer.player_id == user_id,
            PlayerAnswer.is_correct == True
        ).first()
        
        if correct_answer:
            return {
                "is_correct": True,
                "match_status": match.status,
                "winner_id": match.winner_id,
                "message": "You already submitted the correct answer"
            }
        
        # Normalize answers (strip whitespace, lowercase) and handle non-string/None safely
        submitted = str(answer).strip().lower() if answer is not None else ""
        expected_raw = getattr(player_input, 'expected_answer', None)
        expected = str(expected_raw).strip().lower() if expected_raw is not None else ""
        # If expected is not set, treat as incorrect rather than raising
        is_correct = (submitted == expected) and expected != ""
        
        # Calculate time taken
        time_taken = int((datetime.utcnow() - match.started_at).total_seconds()) if match.started_at else None
        
        # Record answer
        player_answer = PlayerAnswer(
            match_id=match.id,
            player_id=user_id,
            puzzle_id=match.puzzle_id,
            submitted_answer=str(answer) if answer is not None else None,
            is_correct=is_correct,
            time_taken_seconds=time_taken
        )
        db.add(player_answer)
        
        # If correct, check if first to solve
        if is_correct and not match.winner_id:
            match.winner_id = user_id
            match.status = 'completed'
            match.completed_at = datetime.utcnow()

            # Safely upsert match_stats for winner and loser to avoid duplicate-insert race
            try:
                # Winner upsert: increment total_matches and matches_won, increment puzzles solved and update times
                winner_params = {
                    'user_id': user_id,
                    'total_matches': 1,
                    'matches_won': 1,
                    'matches_lost': 0,
                    'total_puzzles_solved': 1 if is_correct else 0,
                    'fastest_solve_seconds': time_taken if time_taken is not None else None,
                    'average_solve_seconds': float(time_taken) if time_taken is not None else None,
                }
                upsert_sql = text(
                    "INSERT INTO match_stats (user_id, total_matches, matches_won, matches_lost, total_puzzles_solved, fastest_solve_seconds, average_solve_seconds, current_streak, best_streak, updated_at) "
                    "VALUES (:user_id, :total_matches, :matches_won, :matches_lost, :total_puzzles_solved, :fastest_solve_seconds, :average_solve_seconds, 0, 0, now()) "
                    "ON CONFLICT (user_id) DO UPDATE SET "
                    "total_matches = COALESCE(match_stats.total_matches,0) + EXCLUDED.total_matches, "
                    "matches_won = COALESCE(match_stats.matches_won,0) + EXCLUDED.matches_won, "
                    "matches_lost = COALESCE(match_stats.matches_lost,0) + EXCLUDED.matches_lost, "
                    "total_puzzles_solved = COALESCE(match_stats.total_puzzles_solved,0) + EXCLUDED.total_puzzles_solved, "
                    "fastest_solve_seconds = LEAST(COALESCE(match_stats.fastest_solve_seconds, 9999999), COALESCE(EXCLUDED.fastest_solve_seconds, 9999999)), "
                    "average_solve_seconds = CASE WHEN COALESCE(match_stats.total_puzzles_solved,0) = 0 THEN EXCLUDED.average_solve_seconds "
                    "ELSE ((COALESCE(match_stats.average_solve_seconds,0) * COALESCE(match_stats.total_puzzles_solved,0) + COALESCE(EXCLUDED.average_solve_seconds,0)) / (COALESCE(match_stats.total_puzzles_solved,0) + COALESCE(EXCLUDED.total_puzzles_solved,0))) END, "
                    "updated_at = now()"
                )
                db.execute(upsert_sql, winner_params)

                # Loser upsert: increment total_matches and matches_lost
                opponent_id = match.player1_id if user_id == match.player2_id else match.player2_id
                if opponent_id:
                    loser_params = {
                        'user_id': opponent_id,
                        'total_matches': 1,
                        'matches_won': 0,
                        'matches_lost': 1,
                        'total_puzzles_solved': 0,
                        'fastest_solve_seconds': None,
                        'average_solve_seconds': None,
                    }
                    db.execute(upsert_sql, loser_params)
            except Exception:
                logger.exception("Failed upserting match_stats during submit_answer")

        try:
            db.commit()
        except Exception as e:
            logger.exception("Database commit failed in submit_answer")
            try:
                db.rollback()
            except Exception:
                logger.exception("Rollback also failed")
            raise
        # Notify via websocket about the submission
        try:
            asyncio.create_task(manager.notify_answer_submitted(str(match.id), user_id, is_correct))
        except Exception:
            pass

        # If match completed, notify about completion (include winner username)
        if is_correct and match.status == 'completed' and match.winner_id:
            try:
                winner = db.query(User).filter(User.id == match.winner_id).first()
                winner_username = winner.username if winner else None
                asyncio.create_task(manager.notify_match_completed(str(match.id), match.winner_id, winner_username))
            except Exception:
                pass

        return {
            "is_correct": is_correct,
            "match_status": match.status,
            "winner_id": match.winner_id,
            "time_taken_seconds": time_taken,
            "message": "Correct! You win!" if is_correct and match.winner_id == user_id else
                      "Correct answer!" if is_correct else "Incorrect answer, try again!"
        }
    
    @staticmethod
    def _update_player_stats(db: Session, user_id: int, solve_time: Optional[int], solved: bool):
        """Update player statistics"""
        stats = db.query(MatchStats).filter(MatchStats.user_id == user_id).first()
        
        if not stats:
            stats = MatchStats(user_id=user_id)
            db.add(stats)
        # Ensure numeric fields are initialized
        stats.total_matches = stats.total_matches or 0
        stats.matches_won = stats.matches_won or 0
        stats.matches_lost = stats.matches_lost or 0
        stats.total_puzzles_solved = stats.total_puzzles_solved or 0

        if solved:
            stats.total_puzzles_solved = (stats.total_puzzles_solved or 0) + 1
            
            if solve_time:
                if stats.fastest_solve_seconds is None or solve_time < stats.fastest_solve_seconds:
                    stats.fastest_solve_seconds = solve_time
                
                # Update average safely
                if stats.average_solve_seconds is None:
                    stats.average_solve_seconds = float(solve_time)
                else:
                    total_time = stats.average_solve_seconds * (stats.total_puzzles_solved - 1) + solve_time
                    stats.average_solve_seconds = total_time / stats.total_puzzles_solved

        # Do not commit here; caller should commit to keep transactional integrity
        try:
            db.flush()
        except Exception:
            # If flush fails, log and continue; caller will handle rollback/commit
            logger.exception("Flush failed in _update_player_stats")
    
    @staticmethod
    def get_match_details(db: Session, match_id: str, user_id: int) -> dict:
        """Get detailed match information"""
        match = db.query(Match).filter(Match.id == match_id).first()
        if not match:
            raise ValueError("Match not found")
        
        # Get puzzle
        puzzle = db.query(Puzzle).filter(Puzzle.id == match.puzzle_id).first()
        
        # Get player input
        player_input = db.query(PlayerPuzzleInput).filter(
            PlayerPuzzleInput.match_id == match_id,
            PlayerPuzzleInput.player_id == user_id
        ).first()
        
        # Get usernames
        player1 = db.query(User).filter(User.id == match.player1_id).first() if match.player1_id else None
        player2 = db.query(User).filter(User.id == match.player2_id).first() if match.player2_id else None
        winner = db.query(User).filter(User.id == match.winner_id).first() if match.winner_id else None
        
        return {
            "match": match,
            "puzzle": puzzle,
            "player_input": player_input.input_data if player_input else None,
            "expected_answer": player_input.expected_answer if player_input else None,
            "player1_username": player1.username if player1 else None,
            "player2_username": player2.username if player2 else None,
            "winner_username": winner.username if winner else None,
        }
    
    @staticmethod
    def get_user_matches(db: Session, user_id: int, limit: int = 50) -> List[Match]:
        """Get user's match history"""
        matches = db.query(Match).filter(
            or_(Match.player1_id == user_id, Match.player2_id == user_id)
        ).order_by(Match.created_at.desc()).limit(limit).all()
        
        return matches
    
    @staticmethod
    def get_leaderboard(db: Session, limit: int = 100) -> List[dict]:
        """Get leaderboard"""
        # Prefer DB view `leaderboard` if present, fall back to building from tables
        from sqlalchemy import text
        try:
            query = text('SELECT * FROM leaderboard LIMIT :limit')
            result = db.execute(query, {"limit": limit})
            rows = []
            for row in result:
                # SQLAlchemy Row supports ._mapping for dict-like access
                if hasattr(row, '_mapping'):
                    rows.append(dict(row._mapping))
                else:
                    try:
                        rows.append(dict(row))
                    except Exception:
                        # Fallback to manual conversion
                        rows.append({k: v for k, v in row})

            # Normalize: if a user has 0 matches, show zeros for puzzle stats
            for r in rows:
                try:
                    if int(r.get('total_matches') or 0) == 0:
                        r['total_puzzles_solved'] = 0
                        r['fastest_solve_seconds'] = 0
                        r['average_solve_seconds'] = 0
                except Exception:
                    # If conversion fails, skip normalization for that row
                    pass

            return rows
        except Exception:
            # Fallback: aggregate from match_stats and users
            fallback_q = text(
                "SELECT u.id, u.username, COALESCE(ms.total_matches,0) as total_matches, "
                "COALESCE(ms.matches_won,0) as matches_won, COALESCE(ms.matches_lost,0) as matches_lost, "
                "CASE WHEN COALESCE(ms.total_matches,0) > 0 THEN ROUND((COALESCE(ms.matches_won,0)::float / COALESCE(ms.total_matches,0)::float * 100)::numeric,2) ELSE 0 END as win_rate, "
                "COALESCE(ms.total_puzzles_solved,0) as total_puzzles_solved, ms.fastest_solve_seconds, ms.average_solve_seconds, ms.current_streak, ms.best_streak "
                "FROM users u LEFT JOIN match_stats ms ON u.id = ms.user_id "
                "ORDER BY COALESCE(ms.matches_won,0) DESC, COALESCE(ms.average_solve_seconds,999999) ASC "
                "LIMIT :limit"
            )
            result = db.execute(fallback_q, {"limit": limit})
            rows = []
            for row in result:
                if hasattr(row, '_mapping'):
                    rows.append(dict(row._mapping))
                else:
                    try:
                        rows.append(dict(row))
                    except Exception:
                        rows.append({k: v for k, v in row})

            # Normalize: if a user has 0 matches, show zeros for puzzle stats
            for r in rows:
                try:
                    if int(r.get('total_matches') or 0) == 0:
                        r['total_puzzles_solved'] = 0
                        r['fastest_solve_seconds'] = 0
                        r['average_solve_seconds'] = 0
                except Exception:
                    pass

            return rows
