from flask import Blueprint, jsonify, request

from database import DataManager

get_key_blueprint = Blueprint("get_key", __name__)

@get_key_blueprint.route("/get_key", methods=["POST"])
async def get_key():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    key = await DataManager.get_authentication_key(username)
    
    if key is None:
        key = await DataManager.create_authentication_key(username, password)
        return jsonify({"status": "success, key created", "key": key}), 200
    else:
        return jsonify({"status": "success, key found", "key": key}), 200
