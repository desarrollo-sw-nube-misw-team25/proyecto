from src.commands.base_command import BaseCommand
from flask_jwt_extended import create_access_token
from datetime import timedelta

from src.errors.errors import BadRequestApi, InvalidUsernameOrPassword, Unauthorized
from src.models.user_model import User


class LoginUser(BaseCommand):
    def __init__(self, data) -> None:
        self.email = data["email"]
        self.password = data["password"]

    def execute(self):
        if self.email == None or self.verify_if_none_empty(self.email):
            raise InvalidUsernameOrPassword()
        user = User.query.filter_by(email=self.email).first()
        if not user:
            raise BadRequestApi("The provided email doesn't exist")
        if not user.check_password(self.password):
            raise Unauthorized()
        return create_access_token(
            identity=self.email, expires_delta=timedelta(hours=1)
        )
