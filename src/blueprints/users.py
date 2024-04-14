from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.commands.user_commands.login_user import LoginUser
from src.commands.user_commands.register_user import RegisterUser


users_blueprint = Blueprint("users", __name__)


@users_blueprint.route("/api/auth/login", methods=["GET"])
@jwt_required()
def login_user():
    current_user = get_jwt_identity()
    token = LoginUser().execute()
    return jsonify(token), 200


@users_blueprint.route("/api/auth/signup", methods=["POST"])
def signup_user():
    try:
        user = RegisterUser().execute()
        return jsonify(), 201
    except BadRequest:
        return jsonify()
