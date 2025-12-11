const yourIp = document.getElementById('yourIp').textContent;

// Réinitialiser la session
function resetSession() {
    if (confirm('Voulez-vous créer une nouvelle session avec une nouvelle IP ?')) {
        fetch('/reset')
            .then(res => res.json())
            .then(() => {
                window.location.reload();
            });
    }
}

// Charger les messages
function loadMessages() {
    fetch('/messages')
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById('messagesContainer');
            if (data.messages.length === 0) {
                container.innerHTML = '<div class="no-messages">Aucun message pour le moment...</div>';
                return;
            }
            
            container.innerHTML = data.messages.map(msg => `
                <div class="message">
                    <div class="message-header">
                        <span class="message-ip">De: ${msg.from_ip} → À: ${msg.to_ip}</span>
                        <span>${msg.timestamp}</span>
                    </div>
                    <div class="message-content">${escapeHtml(msg.content)}</div>
                </div>
            `).join('');
            
            container.scrollTop = container.scrollHeight;
        })
        .catch(error => {
            console.error('Erreur lors du chargement des messages:', error);
        });
}

// Échapper le HTML pour éviter les injections XSS
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Envoyer un message
document.getElementById('messageForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const destIp = document.getElementById('destIp').value;
    const message = document.getElementById('message').value;
    
    try {
        const response = await fetch('/send', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                to_ip: destIp,
                content: message
            })
        });
        
        const result = await response.json();
        if (result.success) {
            document.getElementById('message').value = '';
            loadMessages();
        } else {
            alert('Erreur lors de l\'envoi: ' + result.error);
        }
    } catch (error) {
        alert('Erreur de connexion: ' + error.message);
    }
});

// Actualiser les messages toutes les 2 secondes
loadMessages();
setInterval(loadMessages, 2000);
