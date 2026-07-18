
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HTML Reminder Chatbot</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', system-ui, sans-serif; }
        body { background: #f0f2f5; display: flex; justify-content: center; align-items: center; hieght: 100vh; height: 100vh; }
        .chat-container { width: 400px; height: 600px; background: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); display: flex; flex-direction: column; overflow: hidden; }
        .chat-header { background: #0078d4; color: white; padding: 15px; text-align: center; font-weight: bold; }
        .chat-messages { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }
        .message { max-width: 75%; padding: 10px 14px; border-radius: 15px; font-size: 14px; line-height: 1.4; word-wrap: break-word; }
        .bot { background: #e1dfdd; align-self: flex-start; border-bottom-left-radius: 2px; color: #323130; }
        .user { background: #0078d4; color: white; align-self: flex-end; border-bottom-right-radius: 2px; }
        .chat-input-area { display: flex; padding: 10px; background: #faf9f8; border-top: 1px solid #edebe9; }
        #input-box { flex: 1; padding: 10px; border: 1px solid #ccd1d9; border-radius: 20px; outline: none; padding-left: 15px; }
        #send-btn { background: #0078d4; color: white; border: none; padding: 0 15px; margin-left: 8px; border-radius: 20px; cursor: pointer; font-weight: bold; }
        #send-btn:hover { background: #106ebe; }
    </style>
</head>
<body>

<div class="chat-container">
    <div class="chat-header">Reminder Bot</div>
    <div class="chat-messages" id="chat-messages">
        <div class="message bot">Hello! Tell me what to remember and when.<br><br>Format:<br><b>[message] in [X] seconds</b><br><i>Example: Drink water in 10 seconds</i></div>
    </div>
    <div class="chat-input-area">
        <input type="text" id="input-box" placeholder="Type a reminder command..." autocomplete="off">
        <button id="send-btn">Send</button>
    </div>
</div>

<script>
    const chatMessages = document.getElementById('chat-messages');
    const inputBox = document.getElementById('input-box');
    const sendBtn = document.getElementById('send-btn');

    // Load existing reminders from localStorage or initialize empty array
    let reminders = JSON.parse(localStorage.getItem('html_reminders')) || [];

    // Helper to add chat bubbles
    function addMessage(text, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message', sender);
        msgDiv.innerHTML = text;
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight; // Auto scroll to bottom
    }

    // Process user commands
    function processCommand() {
        const text = inputBox.value.trim();
        if (!text) return;

        addMessage(text, 'user');
        inputBox.value = '';

        // Regex pattern to extract message and seconds (e.g., "Call mom in 30 seconds")
        const pattern = /(.+)\s+in\s+(\d+)\s+seconds?/i;
        const match = text.match(pattern);

        if (match) {
            const reminderText = match[1];
            const seconds = parseInt(match[2], 10);
            const triggerTime = Date.now() + (seconds * 1000);

            // Save reminder configuration
            const newReminder = { message: reminderText, triggerTime: triggerTime };
            reminders.push(newReminder);
            localStorage.setItem('html_reminders', JSON.stringify(reminders));

            addMessage(`Got it! I will remind you to "${reminderText}" in ${seconds} seconds.`, 'bot');
        } else {
            addMessage(`Sorry, I didn't catch that. Please use the format:<br><b>[message] in [seconds] seconds</b>`, 'bot');
        }
    }

    // Background checker simulating thread loops (runs every second)
    setInterval(() => {
        const now = Date.now();
        let changed = false;

        reminders = reminders.filter(reminder => {
            if (now >= reminder.triggerTime) {
                addMessage(`⏰ <b>REMINDER:</b> ${reminder.message}`, 'bot');
                // Play native browser notification sound if supported
                try { new Audio('https://mixkit.co').play(); } catch(e){}
                changed = true;
                return false; // Remove from active list
            }
            return true; // Keep in list
        });

        if (changed) {
            localStorage.setItem('html_reminders', JSON.stringify(reminders));
        }
    }, 1000);

    // Event listeners for sending messages
    sendBtn.addEventListener('click', processCommand);
    inputBox.addEventListener('keypress', (e) => { if (e.key === 'Enter') processCommand(); });
</script>

</body>
</html>
