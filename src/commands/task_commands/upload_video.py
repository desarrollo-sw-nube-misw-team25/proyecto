from src.commands.base_command import BaseCommand
from flask_jwt_extended import create_access_token
from datetime import timedelta
from src.extensions import db

from src.errors.errors import InvalidUsernameOrPassword, Unauthorized
from src.models.video_model import Video


class UploadVideo(BaseCommand):
    def __init__(self, video_info) -> None:
        self.data = video_info

    def execute(self):
        new_video = Video(id=self.data['video_id'],filename=self.data['filename'],timestamp=self.data['timestamp'],status=self.data['status'])
        db.session.add(new_video)
        db.session.commit()
        return new_video

