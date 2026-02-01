"""
WebSocket endpoints for real-time match updates
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session
import json
import logging

from app.core.database import get_db
from app.core.security import get_current_user_from_token
from app.services.websocket_manager import manager
from app.core.enums import WebSocketMessageType

router = APIRouter()
logger = logging.getLogger(__name__)
logger = logging.getLogger(__name__)


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
        user = await get_current_user_from_token(token, db)
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
                if message.get("type") == WebSocketMessageType.PING:
                    await manager.send_personal_message(
                        {"type": WebSocketMessageType.PONG},
                        websocket
                    )
                
                elif message.get("type") == WebSocketMessageType.PLAYER_READY:
                    # Broadcast ready status
                    await manager.broadcast_to_match(
                        match_id,
                        {
                            "type": WebSocketMessageType.PLAYER_READY,
                            "user_id": user.id,
                            "username": user.username
                        }
                    )
                
                # Add more message handlers as needed
                
        except WebSocketDisconnect:
            manager.disconnect(websocket)
        except Exception as e:
            logger.error(f"WebSocket error in message loop: {e}", exc_info=True)
            manager.disconnect(websocket)
    
    except Exception as e:
        logger.error(f"WebSocket connection error: {e}", exc_info=True)
        await websocket.close(code=4000, reason=str(e))
