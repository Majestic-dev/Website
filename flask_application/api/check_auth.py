from flask import Blueprint, jsonify, request

from database import DataManager

check_auth_blueprint = Blueprint("check_auth", __name__)

@check_auth_blueprint.route("/check_auth", methods=["POST"])
async def check_auth():
    auth_header = request.headers.get("Authorization")
    if auth_header:
        if await DataManager.check_key(auth_header):
            return jsonify({"success": "You are authenticated"}), 202
        else:
            return jsonify({"error": "Invalid key"}), 401
    else:
        return jsonify({"error": "No Authorization header"}), 400