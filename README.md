
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WhatsApp Reminder Chatbot</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', system-ui, sans-serif; }
        body { background: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .chat-container { width: 400px; height: 600px; background: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); display: flex; flex-direction: column; overflow: hidden; }
        .chat-header { background: #075E54; color: white; padding: 15px; text-align: center; font-weight: bold; }
        .chat-messages { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }
        .message { max-width: 75%; padding: 10px 14px; border-radius: 15px; font-size: 14px; line-height: 1.4; word-wrap: break-word; }
        .bot { background: #e1dfdd; align-self: flex-start; border-bottom-left-radius: 2px; color: #323130; }
        .user { background: #075E54; color: white; align-self: flex-end; border-bottom-right-radius: 2px; }
        .chat-input-area { display: flex; padding: 10px; background: #faf9f8; border-top: 1px solid #edebe9; }
        #input-box { flex: 1; padding: 10px; border: 1px solid #ccd1d9; border-radius: 20px; outline: none; padding-left: 15px; }
        #send-btn { background: #075E54; color: white; border: none; padding: 0 15px; margin-left: 8px; border-radius: 20px; cursor: pointer; font-weight: bold; }
        #send-btn:hover { background: #128C7E; }
    </style>
</head>
<body>

<div class="chat-container">
    <div class="chat-header">WhatsApp Reminder Bot</div>
    <div class="chat-messages" id="chat-messages">
        <div class="message bot">Hello! Type what to remember and when. I will open a WhatsApp chat to send the alert.<br><br>Format:<br><b>[message] in [X] seconds</b><br><i>Example: Drink water in 10 seconds</i></div>
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

    // TARGET WHATSAPP PHONE NUMBER CONFIGURATION
    const TARGET_PHONE = "916363311629"; // Prefixed with country code 91 for India

    let reminders = JSON.parse(localStorage.getItem('wa_reminders')) || [];

    function addMessage(text, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message', sender);
        msgDiv.innerHTML = text;
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Redirects browser context straight to WhatsApp with your prefilled text
    function triggerWhatsAppRedirect(messageText) {
        const encodedText = encodeURIComponent(`⏰ Reminder Bot: ${messageText}`);
        const whatsappUrl = `https://wa.me{TARGET_PHONE}?text=${encodedText}`;
        
        // Open the WhatsApp click-to-chat window cleanly in a new tab
        window.open(whatsappUrl, '_blank');
    }

    function processCommand() {
        const text = inputBox.value.trim();
        if (!text) return;

        addMessage(text, 'user');
        inputBox.value = '';

        const pattern = /(.+)\s+in\s+(\d+)\s+seconds?/i;
        const match = text.match(pattern);

        if (match) {
            const reminderText = match[1];
            const seconds = parseInt(match[2], 10);
            const triggerTime = Date.now() + (seconds * 1000);

            reminders.push({ message: reminderText, triggerTime: triggerTime });
            localStorage.setItem('wa_reminders', JSON.stringify(reminders));

            addMessage(`Got it! I will redirect you to WhatsApp to text yourself about "${reminderText}" in ${seconds} seconds.`, 'bot');
        } else {
            addMessage(`Sorry, use the format:<br><b>[message] in [seconds] seconds</b>`, 'bot');
        }
    }

    // App background checker loop
    setInterval(() => {
        const now = Date.now();
        let changed = false;

        reminders = reminders.filter(reminder => {
            if (now >= reminder.triggerTime) {
                addMessage(`⏰ <b>REDIRECTING TO WHATSAPP:</b> ${reminder.message}`, 'bot');
                
                // Execute the automated click-to-chat action link
                triggerWhatsAppRedirect(reminder.message);
                
                changed = true;
                return false; 
            }
            return true; 
        });

        if (changed) {
            localStorage.setItem('wa_reminders', JSON.stringify(reminders));
        }
    }, 1000);

    sendBtn.addEventListener('click', processCommand);
    inputBox.addEventListener('keypress', (e) => { if (e.key === 'Enter') processCommand(); });
</script>

</body>
</html>
