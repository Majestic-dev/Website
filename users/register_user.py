from flask import Blueprint, jsonify, request
from database import DataManager

register_user_blueprint = Blueprint("register_user", __name__)

@register_user_blueprint.route("/register_user", methods=["POST"])
async def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if await DataManager.sign_up(username, password):
        return jsonify({"status": "success"}), 201
    else:
        return jsonify({"status": "failure"}), 400