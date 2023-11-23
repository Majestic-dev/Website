from flask import Flask, request, jsonify
from database import DataManager

app = Flask(__name__)

@app.route('/api/get_key', methods=['GET'])
async def get_key():
    if "user" in request.json:
        user = request.json["user"]
        if await DataManager.check_user(user):
            key = await DataManager.get_key(user)
            return jsonify({'error': f'You already have a key which is {key}'}), 400
        else:
            key = await DataManager.create_auth_key(user)
            return jsonify({'key': key}), 201
    else:
        return jsonify({'error': 'No user field'}), 400
        
@app.route('/api/check_auth', methods=['POST'])
async def check_auth():
    if request.headers.get("Authorization") is not None:
        if await DataManager.check_key(request.headers["Authorization"]):
            return jsonify({'success': 'You are authenticated'}), 202
        else:
            return jsonify({'error': 'Invalid key'}), 401
    else:
        return jsonify({'error': 'No Authorization header'}), 400
    
@app.route('/api/delete_key', methods=['DELETE'])
async def delete_key():
    if request.headers.get("Authorization") is not None:
        if await DataManager.check_key(request.headers["Authorization"]):
            await DataManager.delete_auth_key(request.headers["Authorization"])
            return jsonify({'success': 'Key deleted'}), 202
        else:
            return jsonify({'error': 'Invalid key'}), 401
    else:
        return jsonify({'error': 'No Authorization header'}), 400

if __name__ == '__main__':
    app.run(debug=True)