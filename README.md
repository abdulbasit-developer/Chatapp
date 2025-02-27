# FastAPI WebSocket Chat App

A real-time chat application built with FastAPI and WebSockets that works across multiple devices on the same network.



## Features

- Real-time messaging with WebSocket technology
- Clean, modern UI inspired by popular messaging apps
- Works across multiple devices on the same network
- Responsive design that adapts to mobile and desktop
- User identification with unique client IDs
- Join/leave notifications
- Message history displayed during the session

## Demo

Run the application locally and open it on multiple browsers or devices to chat in real-time.

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/fastapi-chat-app.git
cd fastapi-chat-app
```

2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages
```bash
pip install -r requirements.txt
```

## Project Structure

```
fastapi-chat-app/
├── main.py              # FastAPI application with embedded HTML/CSS/JS
└── README.md
```

This app is designed with simplicity in mind - all code (Python, HTML, CSS, and JavaScript) is contained in a single `main.py` file for easy deployment.

## Usage

1. Start the server:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

2. Access the chat:
   - On the same computer: Open `http://localhost:8000` or `http://127.0.0.1:8000` in your browser
   - From other devices on the same network: Open `http://YOUR_COMPUTER_IP:8000` in a browser
     (Replace YOUR_COMPUTER_IP with your machine's local IP address, e.g., 192.168.1.5)

3. Start chatting across devices!

## How to Find Your Local IP Address

### Windows
1. Open Command Prompt
2. Type `ipconfig` and press Enter
3. Look for "IPv4 Address" under your active network adapter

### macOS
1. Open Terminal
2. Type `ifconfig | grep "inet "` and press Enter
3. Look for your local IP (usually starts with 192.168 or 10.0)

### Linux
1. Open Terminal
2. Type `ip addr` or `hostname -I` and press Enter
3. Find your local IP address

## Technical Details

This application uses:
- **FastAPI**: A modern, fast web framework for building APIs
- **WebSockets**: For real-time, bidirectional communication
- **HTML/CSS/JavaScript**: For the front-end interface (embedded in the Python file)

### How It Works

1. The server creates a WebSocket endpoint for clients
2. Each client connects with a unique ID (timestamp-based)
3. Messages are broadcasted to all connected clients
4. The server maintains a list of active connections
5. When a client disconnects, a notification is sent to all remaining clients

## Customization

The HTML, CSS, and JavaScript are all defined in the `html` variable in the `main.py` file. To customize the appearance:

1. Modify the CSS section within the `<style>` tags
2. Change the HTML structure as needed
3. Update the JavaScript functionality if necessary

## License

[MIT License](LICENSE)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
