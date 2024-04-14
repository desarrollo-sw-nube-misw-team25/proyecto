from flask import jsonify

from src.extensions import celery, db
import subprocess
from src.models.video_model import Video
def delete_task_id(user_id, id_task):
    # Query the database for the video linked to the given task ID
    video = Video.query.filter_by(task_id=id_task).first()

    if video is None:
        # No video found with that task ID
        return jsonify({'message': 'No video found with the given task ID'}), 404

    try:
        # Revoke the task using Celery
        celery.control.revoke(id_task, terminate=True)

        # Update the state of the video in the database
        video.state = 'deleted'
        db.session.commit()

        return jsonify({'message': 'Task deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
