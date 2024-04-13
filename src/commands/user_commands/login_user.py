from src.commands.base_command import BaseCommand
from flask_jwt_extended import create_access_token
from datetime import timedelta

from src.errors.errors import InvalidUsernameOrPassword, Unauthorized
from src.models.user_model import User


class LoginUser(BaseCommand):
  def __init__(self, username, password) -> None:
    self.username = username
    self.password = password

  def execute(self):
    if(self.email == None or len(self.email) == 0 or self.password == None or len(self.password) == 0):
      raise InvalidUsernameOrPassword()
    user = User.query.filter_by(email=self.email).first()
    if user and not user.check_password(self.password):
      raise Unauthorized()
    return create_access_token(identity=self.email, expires_delta=timedelta(hours=1))