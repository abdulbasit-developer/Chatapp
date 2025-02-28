# FastAPI Chat Application

A real-time chat application built with FastAPI, WebSockets, and vanilla JavaScript that allows users to exchange messages and share files with other connected clients.

## Features

- Real-time messaging using WebSockets
- File sharing functionality
- Unique user IDs for each client
- Message broadcasting to all connected clients
- Modern, responsive UI
- Support for notifications (user join/leave)

## Project Structure

```
fastapi-chat/
├── main.py                  # Application entry point
├── connection_manager.py    # WebSocket connection manager
├── routes.py                # API routes definition
├── static/                  # Static files
│   ├── css/
│   │   └── styles.css       # CSS styles
│   ├── js/
│   │   └── chat.js          # JavaScript code
│   └── index.html           # HTML template
└── uploads/                 # Directory for uploaded files
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fastapi-chat
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# For Windows
venv\Scripts\activate
# For macOS/Linux
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install fastapi uvicorn python-multipart
```

## Running the Application

1. Start the application:
```bash
python main.py
```
Alternatively, you can use Uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

## How It Works

### Backend Components

- **main.py**: Initializes the FastAPI application, mounts static file directories, and configures routes.
- **connection_manager.py**: Manages WebSocket connections, providing methods for connecting, disconnecting, and sending messages.
- **routes.py**: Defines API endpoints for serving the web interface, handling WebSocket connections, and serving uploaded files.

### Frontend Components

- **index.html**: The main HTML template for the chat interface.
- **styles.css**: CSS styling for the chat interface.
- **chat.js**: JavaScript code handling WebSocket connections, sending/receiving messages, and file uploads.

## WebSocket Communication

The application uses WebSockets for real-time bidirectional communication:

1. When a user connects, a unique client ID is assigned based on the current timestamp.
2. Text messages are sent directly over the WebSocket connection.
3. Files are encoded as base64 and sent as JSON objects containing metadata about the file.
4. The server processes incoming messages and broadcasts them to other connected clients.

## File Sharing

1. Users can attach files using the "Attach File" button.
2. Files are uploaded to the server and stored in the `uploads` directory.
3. The server generates a unique filename to prevent collisions.
4. Links to uploaded files appear in the chat for both the sender and recipients.

## Customization

- Change the color scheme by modifying the CSS variables in `styles.css`.
- Adjust the WebSocket connection logic in `chat.js` if deploying behind a proxy.
- Modify the file storage location by changing the `uploads` directory path in `main.py`.



## License

[MIT License](LICENSE)
