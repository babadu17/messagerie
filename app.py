from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import socket
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Stockage des messages en mémoire
messages = []
# Compteur pour simuler différents utilisateurs
user_counter = 0

@app.route('/')
def index():
    # Créer un identifiant unique pour chaque session
    if 'user_id' not in session:
        global user_counter
        user_counter += 1
        session['user_id'] = f"192.168.1.{100 + user_counter}"
    
    user_ip = session['user_id']
    return render_template('index.html', user_ip=user_ip)

@app.route('/send', methods=['POST'])
def send_message():
    try:
        data = request.json
        from_ip = session.get('user_id', 'unknown')
        to_ip = data.get('to_ip')
        content = data.get('content')
        
        if not to_ip or not content:
            return jsonify({'success': False, 'error': 'Données manquantes'})
        
        message = {
            'from_ip': from_ip,
            'to_ip': to_ip,
            'content': content,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }
        
        messages.append(message)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/messages')
def get_messages():
    user_ip = session.get('user_id', 'unknown')
    # Filtrer les messages pour cet utilisateur
    user_messages = [
        msg for msg in messages 
        if msg['from_ip'] == user_ip or msg['to_ip'] == user_ip
    ]
    return jsonify({'messages': user_messages})

@app.route('/reset')
def reset_session():
    session.clear()
    return jsonify({'success': True})

if __name__ == '__main__':
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"\n{'='*50}")
    print(f"🚀 Serveur de messagerie démarré!")
    print(f"📡 IP locale: {local_ip}")
    print(f"🌐 Accédez à: http://{local_ip}:5000")
    print(f"{'='*50}\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
