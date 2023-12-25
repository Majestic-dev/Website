from flask import Blueprint, jsonify, request
from database import DataManager

login_user_blueprint = Blueprint("login_user", __name__)

@login_user_blueprint.route("/login_user", methods=["POST"])
async def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if await DataManager.login_user(username, password):
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "failure"}), 400