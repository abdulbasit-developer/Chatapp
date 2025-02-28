var client_id = Date.now();
document.querySelector("#ws-id").textContent = client_id;

// Use window.location.host for dynamic addressing
var protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
var ws = new WebSocket(`${protocol}//${window.location.host}/ws/${client_id}`);

// Show selected file name
document.getElementById('fileInput').addEventListener('change', function(e) {
    var fileName = e.target.files[0] ? e.target.files[0].name : '';
    document.getElementById('fileName').textContent = fileName;
});

ws.onmessage = function(event) {
    var messages = document.getElementById('messages');
    var message = document.createElement('li');
    
    try {
        // Try to parse as JSON (for file messages)
        var data = JSON.parse(event.data);
        
        // Add appropriate styling based on message sender
        if (data.sender === 'self') {
            message.className = 'message own';
        } else {
            message.className = 'message other';
            
            // Add sender info for messages from others
            var senderInfo = document.createElement('div');
            senderInfo.className = 'sender-info';
            senderInfo.textContent = `Client #${data.client_id}`;
            message.appendChild(senderInfo);
        }
        
        // Add text message if it exists
        if (data.message && data.message.trim() !== '') {
            var textContent = document.createElement('div');
            textContent.className = 'message-content';
            textContent.textContent = data.message;
            message.appendChild(textContent);
        }
        
        // Check if it's a file message
        if (data.type === 'file') {
            var fileLink = document.createElement('a');
            fileLink.href = data.file_url;
            fileLink.className = 'file-attachment';
            fileLink.download = data.filename;
            fileLink.innerHTML = `<span class="file-icon">📎</span> ${data.filename}`;
            message.appendChild(fileLink);
        }
        
    } catch (e) {
        // Handle legacy text format or notifications
        var messageText = event.data;
        
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
    }
    
    messages.appendChild(message);
    
    // Scroll to the bottom to show the latest message
    document.querySelector('.chat-container').scrollTop = document.querySelector('.chat-container').scrollHeight;
};

function sendMessage(event) {
    var input = document.getElementById("messageText");
    var fileInput = document.getElementById("fileInput");
    var messageText = input.value.trim();
    
    // Check if there's a file to send
    if (fileInput.files.length > 0) {
        var file = fileInput.files[0];
        var reader = new FileReader();
        
        reader.onload = function(e) {
            // Send file as a base64 encoded string with metadata
            var fileData = {
                type: 'file',
                filename: file.name,
                content: e.target.result.split(',')[1], // Remove data URL prefix
                file_type: file.type,
                message: messageText // Include the message text
            };
            
            ws.send(JSON.stringify(fileData));
            
            // Reset file input
            fileInput.value = '';
            document.getElementById('fileName').textContent = '';
        };
        
        reader.readAsDataURL(file);
    } 
    // Send text message if there's text but no file
    else if (messageText) {
        ws.send(messageText);
    }
    
    input.value = '';
    
    if (event) {
        event.preventDefault();
    }
}

// Allow sending with Enter key
document.getElementById('messageText').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
