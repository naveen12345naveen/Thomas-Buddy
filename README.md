// App background checker loop
setInterval(() => {
    const now = Date.now();
    let changed = false;

    reminders = reminders.filter(reminder => {
        if (now >= reminder.triggerTime) {
            // Encode message strings safely
            const encodedText = encodeURIComponent(`⏰ Reminder Bot: ${reminder.message}`);
            const whatsappUrl = `https://wa.me{TARGET_PHONE}?text=${encodedText}`;

            // Create a custom notification with a physical click button to bypass security filters
            const buttonHTML = `
                ⚡ <b>REMINDER ALREADY DUE:</b> ${reminder.message}<br><br>
                <a href="${whatsappUrl}" target="_blank" style="
                    display: inline-block; 
                    background: #128C7E; 
                    color: white; 
                    padding: 8px 14px; 
                    border-radius: 20px; 
                    text-decoration: none; 
                    font-weight: bold; 
                    margin-top: 5px;
                    box-shadow: 0 4px 10px rgba(18, 140, 126, 0.3);
                ">Click to Send to WhatsApp</a>
            `;

            addMessage(buttonHTML, 'bot', true);
            
            // Try automatic launch just in case permissions are allowed
            try { window.open(whatsappUrl, '_blank'); } catch(e) { console.log("Blocked automated window popup."); }
            
            changed = true;
            return false; 
        }
        return true; 
    });

    if (changed) {
        localStorage.setItem('wa_reminders', JSON.stringify(reminders));
    }
}, 1000);
