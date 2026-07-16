<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Personal Reminder Bot</title>
    <style>
        /* Futuristic Gradient Background */
        body {
            margin: 0;
            padding: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #0f172a, #1e1b4b);
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }

        /* Glassmorphism Chat Container Centered */
        .chat-container {
            width: 450px;
            height: 600px;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 24px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        /* Glow Header */
        .chat-header {
            padding: 20px;
            background: rgba(255, 255, 255, 0.03);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            text-align: center;
        }

        .chat-header h2 {
            margin: 0;
            font-size: 1.25rem;
            color: #6366f1;
            text-shadow: 0 0 10px rgba(99, 102, 241, 0.5);
            letter-spacing: 1px;
        }

        /* Chat History Stream */
        .chat-logs {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        /* Custom Scrollbar */
        .chat-logs::-webkit-scrollbar {
            width: 6px;
        }
        .chat-logs::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
        }

        /* Message Bubbles */
        .msg {
            padding: 12px 16px;
            border-radius: 16px;
            max-width: 75%;
            font-size: 0.95rem;
            line-height: 1.4;
            animation: fadeIn 0.3s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .msg.bot {
            background: rgba(255, 255, 255, 0.08);
            color: #e2e8f0;
            align-self: flex-start;
            border-bottom-left-radius: 4px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .msg.user {
            background: linear-gradient(135deg, #4f46e5, #6366f1);
            color: #ffffff;
            align-self: flex-end;
            border-bottom-right-radius: 4px;
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
        }

        /* Input Area Wrapper */
        .chat-input-area {
            padding: 20px;
            background: rgba(0, 0, 0, 0.2);
            display: flex;
            gap: 10px;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
        }

        /* Dynamic Input Styles */
        .chat-input-area input {
            flex: 1;
            padding: 12px 16px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            color: #fff;
            font-size: 0.95rem;
            outline: none;
            transition: all 0.3s;
        }

        .chat-input-area input:focus {
            border-color: #6366f1;
            background: rgba(255, 255, 255, 0.08);
            box-shadow: 0 0 10px rgba(99, 102, 241, 0.2);
        }

        /* Neon Action Button */
        .chat-input-area button {
            padding: 12px 24px;
            background: #4f46e5;
            border: none;
            border-radius: 12px;
            color: white;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }

        .chat-input-area button:hover {
            background: #6366f1;
            box-shadow: 0 0 15px rgba(99, 102, 241, 0.6);
        }
    </style>
</head>
<body>

<div class="chat-container">
    <div class="chat-header">
        <h2>⚡ CORE REMINDER ENGINE</h2>
    </div>
    <div id="chat-logs" class="chat-logs"></div>
    <div class="chat-input-area">
        <input type="text" id="chat-input" placeholder="Type here...">
        <button onclick="handleInput()">Send</button>
    </div>
</div>

<script>
    // Conversational state tracking
    let currentStep = 0; 
    let reminderData = { task: "", date: "", time: "" };

    const steps = [
        { key: "task", prompt: "Hello! What event or task should I remind you about?", type: "text" },
        { key: "date", prompt: "Got it. On what date? (YYYY-MM-DD)", type: "date" },
        { key: "time", prompt: "At what time? (HH:MM)", type: "time" }
    ];

    function appendMessage(text, isUser) {
        const logs = document.getElementById('chat-logs');
        const msg = document.createElement('div');
        msg.className = `msg ${isUser ? 'user' : 'bot'}`;
        msg.innerText = text;
        logs.appendChild(msg);
        logs.scrollTop = logs.scrollHeight;
    }

    function initBot() {
        appendMessage(steps[0].prompt, false);
        document.getElementById('chat-input').type = steps[0].type;
    }

    async function handleInput() {
        const inputElement = document.getElementById('chat-input');
        const value = inputElement.value.trim();
        if (!value) return;

        // Display user selection
        appendMessage(value, true);
        reminderData[steps[currentStep].key] = value;
        inputElement.value = "";

        currentStep++;

        if (currentStep < steps.length) {
            // Ask next targeted question
            setTimeout(() => {
                appendMessage(steps[currentStep].prompt, false);
                inputElement.type = steps[currentStep].type;
                inputElement.focus();
            }, 600);
        } else {
            // Process the collected payload data to your C++ backend
            setTimeout(submitReminder, 600);
        }
    }

    async function submitReminder() {
        appendMessage("Processing payload configuration...", false);

        try {
            const response = await fetch('http://localhost:8080/reminder', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(reminderData)
            });
            const data = await response.json();
            appendMessage(data.reply, false);
        } catch (err) {
            appendMessage("⚠️ Failure writing string to local API nod.", false);
        }

        // Reset conversation flow loop
        currentStep = 0;
        reminderData = { task: "", date: "", time: "" };
        setTimeout(initBot, 2000);
    }

    // Capture Enter Keypress
    document.getElementById('chat-input').addEventListener('keypress', function (e) {
        if (e.key === 'Enter') handleInput();
    });

    // Start UI
    initBot();
</script>

</body>
</html>
