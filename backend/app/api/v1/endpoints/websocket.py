"""
WebSocket endpoints for real-time match updates
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session
import json

from app.core.database import get_db
from app.core.security import get_current_user_ws
from app.services.websocket_manager import manager

router = APIRouter()


@router.websocket("/ws/match/{match_id}")
async def websocket_match(
    websocket: WebSocket,
    match_id: str,
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    """
    WebSocket endpoint for real-time match updates
    Query param 'token' should contain the JWT authentication token
    """
    try:
        # Verify user from token
        user = await get_current_user_ws(token, db)
        if not user:
            await websocket.close(code=4001, reason="Unauthorized")
            return
        
        # Connect the user
        await manager.connect(websocket, match_id, user.id)
        
        try:
            while True:
                # Receive messages from client
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Handle different message types
                if message.get("type") == "ping":
                    await manager.send_personal_message(
                        {"type": "pong"},
                        websocket
                    )
                
                elif message.get("type") == "player_ready":
                    # Broadcast ready status
                    await manager.broadcast_to_match(
                        match_id,
                        {
                            "type": "player_ready",
                            "user_id": user.id,
                            "username": user.username
                        }
                    )
                
                # Add more message handlers as needed
                
        except WebSocketDisconnect:
            manager.disconnect(websocket)
        except Exception as e:
            print(f"WebSocket error: {e}")
            manager.disconnect(websocket)
    
    except Exception as e:
        print(f"WebSocket connection error: {e}")
        await websocket.close(code=4000, reason=str(e))
