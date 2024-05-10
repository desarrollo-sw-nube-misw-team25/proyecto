from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..commands.task_commands.create_task import create_task
from ..commands.task_commands.get_all_tasks import get_all_tasks
from ..commands.task_commands.get_task import get_task_id
from ..commands.task_commands.delete_task import delete_task_id
from src.commands.task_commands.upload_video import UploadVideo
import os
import uuid
import subprocess
from datetime import datetime
from celery import Celery
import requests
from google.cloud import storage
from google.oauth2 import service_account

bucket_name = "almacenamiento-videos-nube"
credentials_path = "/app/src/proyecto-sw-nube-c27a18cc403a.json"
tasks_blueprint = Blueprint("tasks", __name__, url_prefix="/api/tasks")
celery = Celery("tasks", backend="redis://redis:6379/0", broker="redis://redis:6379/0")


def upload_video(bucket_name, destination_blob_name, video, credentials_path):

    credentials = service_account.Credentials.from_service_account_file(
        credentials_path
    )
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(video)


def download_video(
    bucket_name, source_blob_name, destination_file_name, credentials_path
):
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path
    )
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)


"""
    - Create a task, requires authentication. 
"""


@tasks_blueprint.route("", methods=["POST"])
@jwt_required()
def post_task():
    data = request.json
    user_id = get_jwt_identity()
    task = create_task(user_id, data)
    return task, 201


"""
    - Geat all user tasks, requires authentication. 
"""


@tasks_blueprint.route("/", methods=["GET"])
@jwt_required()
def get_all_task():
    user_id = get_jwt_identity()
    max_results = request.args.get("max", type=int)
    order = request.args.get("order", type=int, default=0)
    tasks = get_all_tasks(max_results, order)

    return tasks, 200


"""
    - Get a specific task, requires authentcation.
"""


@tasks_blueprint.route("/<id_task>", methods=["GET"])
@jwt_required()
def get_task(id_task):
    user_id = get_jwt_identity()
    task = get_task_id(id_task)
    if task:
        return jsonify(task), 200
    else:
        return jsonify({"message": "Task not found"}), 404


"""
    - Delete a task, requires authentcation.
"""


@tasks_blueprint.route("/<id_task>", methods=["DELETE"])
@jwt_required()
def delete_task(id_task):
    user_id = get_jwt_identity()

    result = delete_task_id(id_task)
    return result


@celery.task()
def process_video(id_video):
    video_id = id_video

    url = f"http://34.71.11.68:5000/procesarVideo/{video_id}"

    response = requests.post(url)

    print(response)


@tasks_blueprint.route("/", methods=["POST"])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    # Retrieve the video file from the request
    video = request.files.get("video")
    if not video:
        return {"error": "No video provided"}, 400

    # Generate a unique ID for the video and create the filename
    video_uuid = uuid.uuid4()
    video_id = str(video_uuid)
    filename = f"unprocessed/{video_id}.mp4"

    # Generate timestamp
    timestamp = datetime.now()

    # The initial status of the video
    status = "uploaded"

    # The video download url
    download_url = "unprocessed"

    # Save to data base
    stored_video = UploadVideo(
        video_uuid, filename, timestamp, status, download_url
    ).execute()
    result = process_video.delay(video_id)
    print("Task ID:", result.id)
    # Return confirmation message
    return (
        jsonify(
            {
                "message": "Video task was created successfully",
                "task": {
                    "id": video_id,
                    "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "status": status,
                },
            }
        ),
        200,
    )
