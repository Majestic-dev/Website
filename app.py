import asyncio
import json

from flask import Flask, Blueprint
from flask_cors import CORS
from flask_application.api.get_key import get_key_blueprint
from flask_application.api.check_auth import check_auth_blueprint
from flask_application.api.delete_key import delete_key_blueprint
from flask_application.api.send_webhook import send_webhook_blueprint

from flask_application.users.login_user import login_user_blueprint
from flask_application.users.register_user import register_user_blueprint

from database import DataManager

app = Flask(__name__)
CORS(app)

api = Blueprint("api", __name__, url_prefix="/api")
users = Blueprint("users", __name__, url_prefix="/users")

api.register_blueprint(get_key_blueprint)
api.register_blueprint(check_auth_blueprint)
api.register_blueprint(delete_key_blueprint)
api.register_blueprint(send_webhook_blueprint)

users.register_blueprint(login_user_blueprint)
users.register_blueprint(register_user_blueprint)

app.register_blueprint(api)
app.register_blueprint(users)

async def main():
    await DataManager.initialise()

if __name__ == "__main__":
    config_file = open("data/config.json")
    host_address = json.load(config_file)["host"]

    if host_address:
        app.run(debug=True)
    else:
        asyncio.run(main())
        print("Please set the host address in data/config.json")