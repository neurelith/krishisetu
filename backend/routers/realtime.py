"""routers/realtime.py — WebSockets-based real-time events router."""

import json
import logging
from typing import List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

logger = logging.getLogger("syngenta.realtime")
router = APIRouter(prefix="/api/ws", tags=["Realtime"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket client connected. Active connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"WebSocket client disconnected. Active connections: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        logger.info(f"Broadcasting message of type '{message.get('type')}' to {len(self.active_connections)} clients.")
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception as exc:
                logger.warning(f"Failed to send websocket message, disconnecting client: {exc}")
                self.disconnect(connection)

manager = ConnectionManager()

@router.websocket("")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Maintain connection and handle any incoming message from client to broadcast
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
                # Broadcast client-sent messages to all tabs
                await manager.broadcast(msg)
            except json.JSONDecodeError:
                pass
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as exc:
        logger.warning(f"WebSocket connection encountered exception: {exc}")
        manager.disconnect(websocket)
