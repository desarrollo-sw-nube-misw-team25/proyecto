from src.commands.base_command import BaseCommand
from src.models.video_model import Video
from src.extensions import Session  # Assuming Session is correctly configured


class UpdateVideo(BaseCommand):
    def __init__(self, id_task, status):
        self.id_task = id_task
        self.status = status

    def execute(self):
        session = Session()
        try:
            # Retrieve the video using the session's query method
            video = session.query(Video).filter_by(id=self.id_task).first()
            if video:
                video.status = self.status
                session.commit()  # Commit the changes# Assuming this returns something relevant
        except Exception as e:
            session.rollback()  # Roll back in case of error
            raise  # Re-raise the exception to handle it further up the call stack
        finally:
            session.close()  # Ensure session is closed after operation
