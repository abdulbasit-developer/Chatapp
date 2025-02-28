from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import json
import base64
import os
import uuid

from connection_manager import manager

def setup_routes(app: FastAPI):
    # Mount static files directory
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    @app.get("/")
    async def get():
        # Read the HTML file from the static directory
        with open("static/index.html", "r") as file:
            html_content = file.read()
        return HTMLResponse(html_content)

    @app.get("/uploads/{filename}")
    async def get_file(filename: str):
        file_path = os.path.join("uploads", filename)
        if os.path.exists(file_path):
            return FileResponse(file_path)
        return {"error": "File not found"}

    @app.websocket("/ws/{client_id}")
    async def websocket_endpoint(websocket: WebSocket, client_id: int):
        await manager.connect(client_id, websocket)
        try:
            while True:
                data = await websocket.receive_text()
                
                # Check if it's a JSON message (file transfer)
                if data.startswith('{'):
                    try:
                        json_data = json.loads(data)
                        
                        # Handle file message
                        if json_data.get('type') == 'file':
                            # Generate unique filename to prevent collisions
                            original_filename = json_data.get('filename', 'unnamed_file')
                            file_extension = os.path.splitext(original_filename)[1]
                            unique_filename = f"{uuid.uuid4()}{file_extension}"
                            file_path = os.path.join("uploads", unique_filename)
                            
                            # Decode base64 and save the file
                            file_content = base64.b64decode(json_data.get('content', ''))
                            with open(file_path, 'wb') as f:
                                f.write(file_content)
                            
                            # Prepare messages
                            file_url = f"/uploads/{unique_filename}"
                            message_text = json_data.get('message', '').strip()
                            
                            # Send confirmation to sender
                            await manager.send_personal_json({
                                "type": "file",
                                "sender": "self",
                                "message": message_text,
                                "filename": original_filename,
                                "file_url": file_url,
                                "client_id": client_id
                            }, client_id)
                            
                            # Broadcast to others
                            await manager.broadcast_json({
                                "type": "file",
                                "sender": "other",
                                "message": message_text,
                                "filename": original_filename,
                                "file_url": file_url,
                                "client_id": client_id
                            }, exclude_client_id=client_id)
                            
                        else:
                            # Unknown JSON format, handle as text
                            await manager.send_personal_message(f"You wrote: {data}", client_id)
                            await manager.broadcast(f"Client #{client_id} says: {data}", exclude_client_id=client_id)
                            
                    except json.JSONDecodeError:
                        # Invalid JSON, handle as text
                        await manager.send_personal_message(f"You wrote: {data}", client_id)
                        await manager.broadcast(f"Client #{client_id} says: {data}", exclude_client_id=client_id)
                else:
                    # Regular text message
                    await manager.send_personal_message(f"You wrote: {data}", client_id)
                    await manager.broadcast(f"Client #{client_id} says: {data}", exclude_client_id=client_id)
                    
        except WebSocketDisconnect:
            manager.disconnect(client_id)
            await manager.broadcast(f"Client #{client_id} left the chat")