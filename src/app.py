from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from src.errors.errors import ApiError
from .blueprints.users import users_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'  # Configure your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional: disables modification tracking

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.register_blueprint(users_blueprint)

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
        "msg": err.description
    }
    return jsonify(response), err.code
