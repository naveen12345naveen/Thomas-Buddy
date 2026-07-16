
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
            color: #fff;
        }

        /* Main Workspace split into Chat and Dashboard */
        .workspace {
            display: flex;
            gap: 30px;
            width: 950px;
            height: 600px;
            max-width: 95%;
        }

        /* Glassmorphism Chat Container */
        .chat-container {
            flex: 1;
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

        /* Saved Reminders Dashboard Panels */
        .dashboard-container {
            width: 380px;
            background: rgba(255, 255, 255, 0.02);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 24px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .chat-header, .dashboard-header {
            padding: 20px;
            background: rgba(255, 255, 255, 0.03);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            text-align: center;
        }

        .chat-header h2, .dashboard-header h2 {
            margin: 0;
            font-size: 1.2rem;
            color: #6366f1;
            text-shadow: 0 0 10px rgba(99, 102, 241, 0.5);
            letter-spacing: 1px;
        }

        /* Chat Streams & List Displays */
        .chat-logs, .reminder-list {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        /* Message Bubbles */
        .msg {
            padding: 12px 16px;
            border-radius: 16px;
            max-width: 75%;
            font-size: 0.95rem;
            line-height: 1.4;
            animation: fadeIn 0.2s ease-out;
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

        /* Live Database Entry Item Cards */
        .reminder-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 14px;
            border-radius: 14px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .reminder-info h4 { margin: 0 0 4px 0; color: #f8fafc; font-size: 0.95rem; }
        .reminder-info span { font-size: 0.8rem; color: #94a3b8; }

        .delete-btn {
            background: rgba(239, 68, 68, 0.2);
            border: 1px solid rgba(239, 68, 68, 0.4);
            color: #fca5a5;
            padding: 6px 12px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.8rem;
            transition: 0.2s;
        }
        .delete-btn:hover { background: #ef4444; color: white; }

        /* Input Controls Setup */
        .chat-input-area {
            padding: 20px;
            background: rgba(0, 0, 0, 0.2);
            display: flex;
            gap: 10px;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
        }

        .chat-input-area input {
            flex: 1;
            padding: 12px 16px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            color: #fff;
            font-size: 0.95rem;
            outline: none;
        }

        .chat-input-area input:focus { border-color: #6366f1; }

        .chat-input-area button {
            padding: 12px 24px;
            background: #4f46e5;
            border: none;
            border-radius: 12px;
            color: white;
            font-weight: 600;
            cursor: pointer;
        }
        .chat-input-area button:hover { background: #6366f1; }
    </style>
</head>
<body>

<div class="workspace">
    <!-- Chat Widget Layout Block -->
    <div class="chat-container">
        <div class="chat-header">
            <h2>⚡ CORE REMINDER BOT</h2>
        </div>
        <div id="chat-logs" class="chat-logs"></div>
        <div class="chat-input-area">
            <input type="text" id="chat-input">
            <button onclick="handleInput()">Send</button>
        </div>
    </div>

    <!-- Active Storage Display Panel -->
    <div class="dashboard-container">
        <div class="dashboard-header">
            <h2>💾 BROWSER LOCAL STORAGE</h2>
        </div>
        <div id="reminder-list" class="reminder-list"></div>
    </div>
</div>

<script>
    let currentStep = 0; 
    let reminderData = { task: "", date: "", time: "" };

    const steps = [
        { key: "task", prompt: "What event or task do you want me to save?", type: "text", placeholder: "e.g., Doctor appointment" },
        { key: "date", prompt: "Got it. What is the target date?", type: "date", placeholder: "" },
        { key: "time", prompt: "At what time?", type: "time", placeholder: "" }
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
        const inputElement = document.getElementById('chat-input');
        inputElement.type = steps[0].type;
        inputElement.placeholder = steps[0].placeholder;
    }

    function handleInput() {
        const inputElement = document.getElementById('chat-input');
        const value = inputElement.value.trim();
        if (!value) return;

        appendMessage(value, true);
        reminderData[steps[currentStep].key] = value;
        inputElement.value = "";

        currentStep++;

        if (currentStep < steps.length) {
            setTimeout(() => {
                appendMessage(steps[currentStep].prompt, false);
                inputElement.type = steps[currentStep].type;
                inputElement.placeholder = steps[currentStep].placeholder;
                inputElement.focus();
            }, 500);
        } else {
            setTimeout(processAndStoreReminder, 500);
        }
    }

    function processAndStoreReminder() {
        // Retrieve existing database array or create fresh blank structure
        let localDb = JSON.parse(localStorage.getItem('my_reminders')) || [];
        
        // Add new reminder payload
        localDb.push({
            id: Date.now(), // Unique identity ID marker
            task: reminderData.task,
            date: reminderData.date,
            time: reminderData.time
        });

        // Commit modifications back directly into browser's native database
        localStorage.setItem('my_reminders', JSON.stringify(localDb));

        appendMessage(`🎉 Success! Saved directly to your local file vault.`, false);
        
        // Re-render dashboard display component view list
        renderDashboardList();

        // Restart interaction loop chain
        currentStep = 0;
        reminderData = { task: "", date: "", time: "" };
        setTimeout(initBot, 2500);
    }

    function renderDashboardList() {
        const container = document.getElementById('reminder-list');
        container.innerHTML = "";
        
        let localDb = JSON.parse(localStorage.getItem('my_reminders')) || [];

        if(localDb.length === 0) {
            container.innerHTML = `<div style="text-align:center; color:#64748b; margin-top:20px; font-size:0.9rem;">No active reminders saved.</div>`;
            return;
        }

        localDb.forEach(item => {
            const card = document.createElement('div');
            card.className = "reminder-card";
            card.innerHTML = `
                <div class="reminder-info">
                    <h4>${item.task}</h4>
                    <span>📅 ${item.date} @ ${item.time}</span>
                </div>
                <button class="delete-btn" onclick="deleteReminder(${item.id})">Clear</button>
            `;
            container.appendChild(card);
        });
    }

    function deleteReminder(id) {
        let localDb = JSON.parse(localStorage.getItem('my_reminders')) || [];
        // Filter out selected ID index entry points
        localDb = localDb.filter(item => item.id !== id);
        localStorage.setItem('my_reminders', JSON.stringify(localDb));
        renderDashboardList();
    }

    document.getElementById('chat-input').addEventListener('keypress', function (e) {
