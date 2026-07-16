<!-- HTML Chatbox Layout -->
<div id="chat-box" style="position:fixed; bottom:20px; right:20px; width:300px; height:400px; border:1px solid #ccc; background:#fff; display:flex; flex-direction:column; font-family:sans-serif; box-shadow:0 4px 8px rgba(0,0,0,0.1); border-radius:8px; overflow:hidden;">
    <div style="background:#007BFF; color:#fff; padding:10px; font-weight:bold;">🕒 Reminder Chatbot</div>
    <div id="chat-logs" style="flex:1; padding:10px; overflow-y:auto; display:flex; flex-direction:column; gap:8px;"></div>
    <div style="display:flex; border-top:1px solid #ccc;">
        <input type="text" id="chat-input" placeholder="e.g., Remind me to stretch in 10s" style="flex:1; padding:10px; border:none; outline:none;">
        <button onclick="sendMessage()" style="padding:10px; background:#007BFF; color:#fff; border:none; cursor:pointer;">Send</button>
    </div>
</div>

<script>
function appendMessage(text, isUser) {
    const logs = document.getElementById('chat-logs');
    const msg = document.createElement('div');
    msg.innerText = text;
    msg.style.padding = '8px 12px';
    msg.style.borderRadius = '15px';
    msg.style.maxWidth = '80%';
    msg.style.alignSelf = isUser ? 'flex-end' : 'flex-start';
    msg.style.background = isUser ? '#007BFF' : '#E5E5EA';
    msg.style.color = isUser ? '#fff' : '#000';
    logs.appendChild(msg);
    logs.scrollTop = logs.scrollHeight;
}

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const text = input.value.trim();
    if (!text) return;

    appendMessage(text, true);
    input.value = '';

    // Send data to your backend server
    try {
        const response = await fetch('http://localhost:8080/reminder', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        const data = await response.json();
        appendMessage(data.reply, false);
        
        // Trigger actual browser alarm if backend returns immediate wait time
        if (data.delay_seconds > 0) {
            setTimeout(() => {
                alert(`🔔 REMINDER: ${data.task}`);
            }, data.delay_seconds * 1000);
        }
    } catch (err) {
        appendMessage("Error connecting to server.", false);
    }
}
</script>
