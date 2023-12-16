from flask import Blueprint, jsonify, request

from database import DataManager

get_key_blueprint = Blueprint("get_key", __name__)

@get_key_blueprint.route("/api/get_key", methods=["GET"])
async def get_key():
    user = request.get_json().get("user")
    if user:
        if await DataManager.check_user(user):
            key = await DataManager.get_key(user)
            return jsonify({"error": f"You already have a key which is {key}"}), 400
        else:
            key = await DataManager.create_auth_key(user)
            return jsonify({"key": key}), 201
    else:
        return jsonify({"error": "No user field"}), 400