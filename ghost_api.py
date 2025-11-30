from flask import Flask, request, jsonify
from datetime import datetime
import threading
import time
from garena_client import GarenaClient
from config import Config

app = Flask(__name__)

# إحصائيات API
api_stats = {
    'start_time': datetime.now(),
    'total_requests': 0,
    'successful_ghost_attacks': 0,
    'failed_attacks': 0,
    'main_account': Config.MAIN_ACCOUNT_ID
}

# اتصال اللعبة الحقيقي
game_client = GarenaClient(Config.MAIN_ACCOUNT_ID, Config.MAIN_ACCOUNT_PASSWORD)

@app.before_request
def before_request():
    api_stats['total_requests'] += 1

@app.route('/')
def home():
    return jsonify({
        'status': 'success',
        'message': '🚀 DRAGON Real Ghost API is running',
        'version': 'REAL-2.0',
        'author': 'DRAGON',
        'account': Config.MAIN_ACCOUNT_ID,
        'region': Config.REGION,
        'mode': 'REAL GHOST PACKETS',
        'endpoints': {
            'ghost_attack': 'GET /ghost?name=GHOST_NAME&team_code=TEAM_CODE',
            'status': 'GET /status',
            'connect': 'GET /connect'
        }
    })

@app.route('/ghost', methods=['GET'])
def ghost_attack():
    """هجوم الشبح الحقيقي"""
    try:
        team_code = request.args.get('team_code')
        ghost_name = request.args.get('name', 'DRAGON Ghost')
        
        if not team_code:
            return jsonify({
                'status': 'error',
                'message': 'Team code is required'
            }), 400
        
        if len(team_code) < 6 or not team_code.isdigit():
            return jsonify({
                'status': 'error',
                'message': 'Invalid team code'
            }), 400
        
        # إرسال الشبح الحقيقي
        success, message = game_client.send_real_ghost(team_code, ghost_name)
        
        if success:
            api_stats['successful_ghost_attacks'] += 1
            return jsonify({
                'status': 'success',
                'message': message,
                'team_code': team_code,
                'ghost_name': ghost_name,
                'account_used': Config.MAIN_ACCOUNT_ID,
                'packet_type': 'REAL GHOST PACKET',
                'timestamp': datetime.now().isoformat()
            })
        else:
            api_stats['failed_attacks'] += 1
            return jsonify({
                'status': 'error',
                'message': message
            }), 500
            
    except Exception as e:
        api_stats['failed_attacks'] += 1
        return jsonify({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }), 500

@app.route('/connect', methods=['GET'])
def connect_game():
    """الاتصال باللعبة"""
    try:
        success = game_client.connect_to_game()
        
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Connected to Free Fire successfully',
                'account': Config.MAIN_ACCOUNT_ID,
                'connected': True,
                'packets_ready': True
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to connect to Free Fire',
                'connected': False
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Connection error: {str(e)}'
        }), 500

@app.route('/status', methods=['GET'])
def status():
    """حالة النظام"""
    return jsonify({
        'status': 'success',
        'api_name': 'DRAGON Real Ghost API',
        'version': 'REAL-2.0',
        'account': Config.MAIN_ACCOUNT_ID,
        'game_connected': game_client.is_connected,
        'real_packets': True,
        'stats': api_stats,
        'uptime': str(datetime.now() - api_stats['start_time'])
    })

def background_maintenance():
    """الصيانة الخلفية"""
    while True:
        try:
            if not game_client.is_connected:
                game_client.connect_to_game()
            time.sleep(60)
        except:
            time.sleep(30)

if __name__ == '__main__':
    # بدء الصيانة الخلفية
    maintenance_thread = threading.Thread(target=background_maintenance, daemon=True)
    maintenance_thread.start()
    
    print("🚀 Starting DRAGON Real Ghost API v2.0...")
    print(f"🎮 Account: {Config.MAIN_ACCOUNT_ID}")
    print(f"🌍 Region: {Config.REGION}")
    print(f"🔧 Mode: REAL GHOST PACKETS")
    
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)