from src.commands.base_command import BaseCommand


class RegisterUser(BaseCommand):
  def __init__(self, user_info):
    self.data = user_info

  def execute(self):
    return super().execute()  