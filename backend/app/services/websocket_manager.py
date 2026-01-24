"""
WebSocket Manager for Real-time Match Updates
Handles live communication between players during matches
"""

from typing import Dict, Set
from fastapi import WebSocket
import json
import asyncio


class ConnectionManager:
    def __init__(self):
        # Map of match_id -> set of websocket connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        # Map of websocket -> (match_id, user_id)
        self.connection_info: Dict[WebSocket, tuple] = {}
    
    async def connect(self, websocket: WebSocket, match_id: str, user_id: int):
        """Accept a new WebSocket connection for a match"""
        await websocket.accept()
        
        if match_id not in self.active_connections:
            self.active_connections[match_id] = set()
        
        self.active_connections[match_id].add(websocket)
        self.connection_info[websocket] = (match_id, user_id)
        
        # Notify others in the match
        await self.broadcast_to_match(match_id, {
            "type": "player_connected",
            "user_id": user_id,
            "timestamp": asyncio.get_event_loop().time()
        }, exclude=websocket)
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection"""
        if websocket in self.connection_info:
            match_id, user_id = self.connection_info[websocket]
            
            if match_id in self.active_connections:
                self.active_connections[match_id].discard(websocket)
                
                # Clean up empty match rooms
                if not self.active_connections[match_id]:
                    del self.active_connections[match_id]
            
            del self.connection_info[websocket]
            
            # Notify others
            asyncio.create_task(
                self.broadcast_to_match(match_id, {
                    "type": "player_disconnected",
                    "user_id": user_id
                })
            )
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send a message to a specific connection"""
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            print(f"Error sending message: {e}")
            self.disconnect(websocket)
    
    async def broadcast_to_match(self, match_id: str, message: dict, exclude: WebSocket = None):
        """Broadcast a message to all connections in a match"""
        if match_id not in self.active_connections:
            return
        
        disconnected = []
        for connection in self.active_connections[match_id]:
            if connection == exclude:
                continue
            
            try:
                await connection.send_text(json.dumps(message))
            except Exception as e:
                print(f"Error broadcasting: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for connection in disconnected:
            self.disconnect(connection)
    
    async def notify_match_start(self, match_id: str, match_data: dict):
        """Notify all players that the match has started"""
        await self.broadcast_to_match(match_id, {
            "type": "match_started",
            "match_id": match_id,
            "started_at": match_data.get("started_at"),
            "puzzle": match_data.get("puzzle")
        })
    
    async def notify_answer_submitted(self, match_id: str, user_id: int, is_correct: bool):
        """Notify when a player submits an answer"""
        await self.broadcast_to_match(match_id, {
            "type": "answer_submitted",
            "user_id": user_id,
            "is_correct": is_correct
        })
    
    async def notify_match_completed(self, match_id: str, winner_id: int, winner_username: str):
        """Notify when a match is completed"""
        await self.broadcast_to_match(match_id, {
            "type": "match_completed",
            "match_id": match_id,
            "winner_id": winner_id,
            "winner_username": winner_username
        })
    
    async def send_heartbeat(self, match_id: str):
        """Send periodic heartbeat to keep connections alive"""
        await self.broadcast_to_match(match_id, {
            "type": "heartbeat",
            "timestamp": asyncio.get_event_loop().time()
        })
    
    def get_match_players_count(self, match_id: str) -> int:
        """Get number of connected players in a match"""
        if match_id not in self.active_connections:
            return 0
        return len(self.active_connections[match_id])


# Global connection manager instance
manager = ConnectionManager()
