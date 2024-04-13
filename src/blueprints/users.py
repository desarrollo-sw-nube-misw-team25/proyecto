from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.commands.user_commands.login_user import LoginUser


users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/users/login', methods = ['GET'])
@jwt_required()
def login_user():
  current_user = get_jwt_identity()
  token = LoginUser().execute()
  return jsonify(token), 201