from flask import Flask, request, jsonify
from database import DataManager

app = Flask(__name__)

@app.route('/api/get_key', methods=['GET'])
async def get_key():
    if await DataManager.check_user(request.remote_addr):
        key = await DataManager.get_key(request.remote_addr)
        return jsonify({'error': f'You already have a key which is {key}'}), 400
    else:
        key = await DataManager.create_auth_key(request.remote_addr)
        return jsonify({'key': key}), 201
    
@app.route('/api/check_auth', methods=['POST'])
async def check_auth():
    if request.method == 'POST':
        if request.headers.get("Authorization") is not None:
            if await DataManager.check_key(request.headers["Authorization"]):
                return jsonify({'success': 'You are authenticated'}), 202
            else:
                return jsonify({'error': 'Invalid key'}), 401
        else:
            return jsonify({'error': 'No Authorization header'}), 400

if __name__ == '__main__':
    app.run(debug=True)