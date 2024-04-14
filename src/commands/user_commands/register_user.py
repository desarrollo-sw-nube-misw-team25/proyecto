import re
from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequestApi
from src.models.user_model import User
from src.extensions import db


class RegisterUser(BaseCommand):
    def __init__(self, user_info):
        self.data = user_info

    def execute(self):
        if "username" not in self.data or self.verify_object_valid(
            self.data["username"]
        ):
            raise BadRequestApi("Username is invalid")
        if "password1" not in self.data or self.verify_if_none_empty(
            self.data["password1"]
        ):
            raise BadRequestApi("Password is invalid")
        if "password2" not in self.data or self.verify_if_none_empty(
            self.data["password2"]
        ):
            raise BadRequestApi(
                "The confirmation password doesn't match the original password"
            )
        if "email" not in self.data or self.verify_if_none_empty(self.data["email"]):
            raise BadRequestApi("Email is invalid")
        self.verify_email()
        self.verify_password()
        new_user = User(username=self.data["username"], email=self.data["email"])
        new_user.set_password(self.data["password1"])
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def verify_email(self):
        # Regular expression for validating an Email
        email_regex = r"^[a-z0-9]+[\._]?[a-z0-9]+@\w+[.]\w+$"

        # Retrieve the email from data
        email = self.data.get("email")

        # Validate the email using the regular expression
        if not re.match(email_regex, email, re.IGNORECASE):
            raise BadRequestApi("The povided email doesn't match our email validations")

        existing_email = User.query.filter_by(email=self.data["email"]).first()
        if existing_email != None:
            raise BadRequestApi("The email is already in use. Try with another email.")
        return True

    def verify_password(self):
        password1 = self.data.get("password1")
        password2 = self.data.get("password2")

        # Check if both passwords are the same
        if password1 != password2:
            return False

        # Regular expression for password validation
        # This regex checks for at least one uppercase letter, one number, and one special character
        password_regex = (
            r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};\'":\\|,.<>\/?]).+$'
        )

        # Validate the password using the regular expression
        if re.match(password_regex, password1):
            return True
        else:
            return False
