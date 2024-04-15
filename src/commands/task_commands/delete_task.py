import os
import uuid

from flask import jsonify
from sqlalchemy import null

from src.extensions import celery, db
import subprocess
from src.models.video_model import Video

unprocessed_video_folder_path = os.path.join('videos', 'unprocessed')
processed_video_folder_path = os.path.join('videos', 'processed')

def delete_task_id(id_task: str):
    uuid_id = uuid.UUID(id_task)

    # Query the database for the video linked to the given task ID
    video = Video.query.filter_by(id=uuid_id).first()

    if video is None:
        # No video found with that task ID
        return jsonify({'message': 'No video found with the given task ID'}), 404

    if video.status == 'deleted':
        # No video found with that task ID
        return jsonify({'message': 'The video was already deleted'}), 404


    try:
        # Delete the unprocessed video file from the folder
        unprocessed_file = os.path.join(unprocessed_video_folder_path, video.filename)

        if os.path.exists(unprocessed_file):
            os.remove(unprocessed_file)

        # Delete the processed video file from the folder
        processed_file = os.path.join(processed_video_folder_path, video.filename)
        if os.path.exists(processed_file):
            os.remove(processed_file)

        # Update the state of the video in the database
        #Video.set_status(video.id, 'deleted')

        # TODO: MODIFY THIS WHEN I MODIFY THE STORAGE FORM
        # moded_video = Video.query.filter_by(id=uuid_id).first()

        return jsonify({'message': 'Task deleted successfully', 'status': 'deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
