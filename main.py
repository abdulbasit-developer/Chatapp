from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>FastAPI Chat</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            }
            
            body {
                background-color: #f0f2f5;
                height: 100vh;
                display: flex;
                flex-direction: column;
            }
            
            .header {
                background-color: #4267B2;
                color: white;
                padding: 15px;
                text-align: center;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            
            .user-id {
                background-color: white;
                color: #333;
                padding: 8px;
                border-radius: 20px;
                display: inline-block;
                margin-top: 5px;
                font-size: 0.9em;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            }
            
            .chat-container {
                flex: 1;
                padding: 20px;
                overflow-y: auto;
                display: flex;
                flex-direction: column;
            }
            
            .message-list {
                list-style-type: none;
                margin-bottom: 70px;
            }
            
            .message {
                margin-bottom: 10px;
                max-width: 80%;
                padding: 10px 15px;
                border-radius: 18px;
                position: relative;
                clear: both;
                word-wrap: break-word;
            }
            
            .message.own {
                background-color: #0084ff;
                color: white;
                float: right;
                border-bottom-right-radius: 5px;
            }
            
            .message.other {
                background-color: #e4e6eb;
                color: #050505;
                float: left;
                border-bottom-left-radius: 5px;
            }
            
            .sender-info {
                font-size: 0.8em;
                color: #65676b;
                margin-bottom: 4px;
            }
            
            .input-container {
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                background-color: white;
                padding: 15px;
                display: flex;
                box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
            }
            
            #messageText {
                flex: 1;
                border: none;
                background-color: #f0f2f5;
                border-radius: 20px;
                padding: 12px 15px;
                font-size: 16px;
                outline: none;
            }
            
            button {
                background-color: #4267B2;
                color: white;
                border: none;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                margin-left: 10px;
                cursor: pointer;
                font-size: 18px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            button:hover {
                background-color: #365899;
            }
            
            .notification {
                text-align: center;
                margin: 10px 0;
                color: #65676b;
                font-style: italic;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>FastAPI Chat</h1>
            <div class="user-id">Your ID: <span id="ws-id"></span></div>
        </div>
        
        <div class="chat-container">
            <ul id="messages" class="message-list"></ul>
        </div>
        
        <form class="input-container" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" placeholder="Type a message..." autocomplete="off"/>
            <button type="submit">➤</button>
        </form>
        
        <script>
            var client_id = Date.now();
            document.querySelector("#ws-id").textContent = client_id;
            
            // Use window.location.host for dynamic addressing
            var protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            var ws = new WebSocket(`${protocol}//${window.location.host}/ws/${client_id}`);
            
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages');
                var message = document.createElement('li');
                var messageText = event.data;
                
                // Add appropriate styling based on message content
                if (messageText.startsWith('You wrote:')) {
                    message.className = 'message own';
                    messageText = messageText.replace('You wrote:', '').trim();
                } else if (messageText.includes('left the chat')) {
                    message.className = 'notification';
                } else {
                    message.className = 'message other';
                    var senderInfo = document.createElement('div');
                    senderInfo.className = 'sender-info';
                    senderInfo.textContent = messageText.split('says:')[0].trim();
                    message.appendChild(senderInfo);
                    messageText = messageText.split('says:')[1].trim();
                }
                
                var content = document.createTextNode(messageText);
                message.appendChild(content);
                messages.appendChild(message);
                
                // Scroll to the bottom to show the latest message
                document.querySelector('.chat-container').scrollTop = document.querySelector('.chat-container').scrollHeight;
            };
            
            function sendMessage(event) {
                var input = document.getElementById("messageText");
                if (input.value.trim()) {
                    ws.send(input.value);
                    input.value = '';
                }
                event.preventDefault();
            }
        </script>
    </body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")