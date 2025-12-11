from flask import Flask, render_template, request, jsonify
from datetime import datetime
import socket

app = Flask(__name__)

# Stockage des messages en mémoire
messages = []

@app.route('/')
def index():
    user_ip = request.remote_addr
    return render_template('index.html', user_ip=user_ip)

@app.route('/send', methods=['POST'])
def send_message():
    try:
        data = request.json
        from_ip = request.remote_addr
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
    user_ip = request.remote_addr
    # Filtrer les messages pour cet utilisateur
    user_messages = [
        msg for msg in messages 
        if msg['from_ip'] == user_ip or msg['to_ip'] == user_ip
    ]
    return jsonify({'messages': user_messages})

if __name__ == '__main__':
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"\n{'='*50}")
    print(f"🚀 Serveur de messagerie démarré!")
    print(f"📡 IP locale: {local_ip}")
    print(f"🌐 Accédez à: http://{local_ip}:5000")
    print(f"{'='*50}\n")
    app.run(host='0.0.0.0', port=5000, debug=True)