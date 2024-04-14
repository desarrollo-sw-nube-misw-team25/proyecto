import os
import uuid

from flask import jsonify

from src.extensions import celery, db
import subprocess
from src.models.video_model import Video


def delete_task_id(id_task: str):
    uuid_id = uuid.UUID(id_task)

    # Query the database for the video linked to the given task ID
    video = Video.query.filter_by(id=uuid_id).first()

    if video is None:
        # No video found with that task ID
        return jsonify({'message': 'No video found with the given task ID'}), 404

    try:
        # Revoke the task using Celery
        celery.control.revoke(uuid_id, terminate=True)

        # Update the state of the video in the database
        # video.state = 'deleted'
        Video.set_status(video.id, 'deleted')

        # Delete the video file from the server
        video_path = os.path.join('videos', video.filename)
        os.remove(video_path)

        # TODO: MODIFY THIS WHEN I MODIFY THE STORAGE FORM
        moded_video = Video.query.filter_by(id=uuid_id).first()

        return jsonify({'message': 'Task deleted successfully', 'status': moded_video.status}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
