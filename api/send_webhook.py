from flask import Blueprint, jsonify, request

import requests

send_webhook_blueprint = Blueprint("send_webhook", __name__)

@send_webhook_blueprint.route("/send_webhook", methods=["POST"])
async def send_webhook():
    webhook_url = request.get_json().get("webhook_url")
    data = request.get_json()
    del data["webhook_url"]
    if webhook_url:
        try:
            requests.post(webhook_url, data)
            return jsonify({"success": "Webhook sent"}), 202
        except:
            return jsonify({"error": "Invalid webhook url"}), 400
    else:
        return jsonify({"error": "No webhook_url or content field"}), 400