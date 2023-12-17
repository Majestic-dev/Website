from flask import Blueprint, jsonify, request

from database import DataManager

delete_key_blueprint = Blueprint("delete_key", __name__)

@delete_key_blueprint.route("/delete_key", methods=["DELETE"])
async def delete_key():
    auth_header = request.headers.get("Authorization")
    if auth_header:
        if await DataManager.check_key(auth_header):
            await DataManager.delete_auth_key(auth_header)
            return jsonify({"success": "Key deleted"}), 202
        else:
            return jsonify({"error": "Invalid key"}), 401
    else:
        return jsonify({"error": "No Authorization header"}), 400
