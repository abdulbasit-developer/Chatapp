from fastapi import WebSocket
from typing import Optional


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, client_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: int):
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def send_personal_message(self, message: str, client_id: int):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)

    async def send_personal_json(self, data: dict, client_id: int):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_json(data)

    async def broadcast(self, message: str, exclude_client_id: Optional[int] = None):
        for client_id, connection in self.active_connections.items():
            if exclude_client_id is None or client_id != exclude_client_id:
                await connection.send_text(message)

    async def broadcast_json(self, data: dict, exclude_client_id: Optional[int] = None):
        for client_id, connection in self.active_connections.items():
            if exclude_client_id is None or client_id != exclude_client_id:
                await connection.send_json(data)


# Create a global instance
manager = ConnectionManager()