from src.commands.base_command import BaseCommand
from flask_jwt_extended import create_access_token
from datetime import timedelta
from src.extensions import db

from src.errors.errors import InvalidUsernameOrPassword, Unauthorized
from src.models.video_model import Video


class UploadVideo(BaseCommand):
    def __init__(self, identification, filename, timestamp, status) -> None:
        self.id = identification
        self.filename = filename
        self.timestamp = timestamp
        self.status = status

    def execute(self):
        new_video = Video(id=self.id, filename=self.filename, timestamp=self.timestamp, status=self.status)
        db.session.add(new_video)
        db.session.commit()
        return new_video
