import os
import requests
import json
from flask import Flask, jsonify
from dotenv import load_dotenv
from src.errors.errors import ApiError
from src.extensions import db, bcrypt, jwt
from src.blueprints.users import users_blueprint
from src.blueprints.tasks import tasks_blueprint

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

app.register_blueprint(users_blueprint)
app.register_blueprint(tasks_blueprint)

db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)


@app.errorhandler(ApiError)
def handle_exception(err):
    response = {"msg": err.description}
    return jsonify(response), err.code


# Move table creation outside of __main__ block
with app.app_context():
    db.create_all()
    file_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
    if not os.path.exists(file_path):
        data = requests.get(url=os.getenv("CREDENTIALS_REQUEST"))
        credentials = data.json()
        with open(file_path, "w") as file:
            json.dump(credentials.get("record"), file, indent=4)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
