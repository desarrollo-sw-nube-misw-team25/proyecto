from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.commands.user_commands.login_user import LoginUser
from src.commands.user_commands.register_user import RegisterUser
from src.errors.errors import BadRequestApi


users_blueprint = Blueprint("users", __name__)


@users_blueprint.route("/api/auth/login", methods=["GET"])
def login_user():
    try:
        token = LoginUser(request.get_json()).execute()
        return jsonify(access_token=token), 200
    except BadRequestApi as e:
        # Specific handling for your custom BadRequestApi exception
        return jsonify({"error": e.description}), 400
    except Exception as e:
        # General exception handling
        return jsonify({"error": str(e)}), 500


@users_blueprint.route("/api/auth/signup", methods=["POST"])
def signup_user():
    try:
        user = RegisterUser(request.get_json()).execute()
        return jsonify(user), 201
    except BadRequestApi as e:
        # Specific handling for your custom BadRequestApi exception
        return jsonify({"error": e.description}), 400
    except Exception as e:
        # General exception handling
        return jsonify({"error": str(e)}), 500