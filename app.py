from flask import Flask, Blueprint
from api.get_key import get_key_blueprint
from api.check_auth import check_auth_blueprint
from api.delete_key import delete_key_blueprint

app = Flask(__name__)

api = Blueprint("api", __name__, url_prefix="/api")

api.register_blueprint(get_key_blueprint)
api.register_blueprint(check_auth_blueprint)
api.register_blueprint(delete_key_blueprint)

app.register_blueprint(api)

if __name__ == "__main__":
    app.run(debug=True)