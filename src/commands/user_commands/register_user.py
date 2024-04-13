from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequestApi


class RegisterUser(BaseCommand):
  def __init__(self, user_info):
    self.data = user_info

  def execute(self):
    if 'username' not in self.data or self.verify_object_valid(self.data['username']):
      raise BadRequestApi('Username is invalid')
    if 'password1' not in self.data or self.verify_if_none_empty(self.data['password1']):
      raise BadRequestApi('Password is invalid')
    if 'password2' not in self.data or self.verify_if_none_empty(self.data['password2']):
      raise BadRequestApi("The confirmation password doesn't match the original password")
    if 'email' not in self.data or self.verify_if_none_empty(self.data['email']):
      raise BadRequestApi('Email is invalid')
  

  def verify_email(self):
    pass
  
  def verify_password(self):
    pass
  