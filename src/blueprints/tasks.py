from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..commands.task_commands.create_task import create_task
from ..commands.task_commands.get_all_tasks import get_all_tasks
from ..commands.task_commands.get_task import get_task_id
from ..commands.task_commands.delete_task import delete_task_id
from src.commands.task_commands.upload_video import UploadVideo
import os
import uuid
from datetime import datetime

tasks_blueprint = Blueprint('tasks', __name__, url_prefix='/api/tasks')
video_folder_path = 'videos'

'''
    - Create a task, requires authentication. 
'''


@tasks_blueprint.route('', methods=['POST'])
@jwt_required()
def post_task():
    data = request.json
    user_id = get_jwt_identity()
    task = create_task(user_id, data)
    return task, 201


'''
    - Geat all user tasks, requires authentication. 
'''


@tasks_blueprint.route('/', methods=['GET'])
@jwt_required()
def get_all_task():
    user_id = get_jwt_identity()
    max_results = request.args.get('max', type=int)
    order = request.args.get('order', type=int, default=0)
    tasks = get_all_tasks(max_results, order)

    return tasks, 200

'''
    - Get a specific task, requires authentcation.
'''


@tasks_blueprint.route('/<id_task>', methods=['GET'])
@jwt_required()
def get_task(id_task):
    user_id = get_jwt_identity()
    task = get_task_id(user_id, id_task)
    if task:
        return jsonify(task), 200
    else:
        return jsonify({"message": "Task not found"}), 404


'''
    - Delete a task, requires authentcation.
'''


@tasks_blueprint.route('/<id_task>', methods=['DELETE'])
@jwt_required()
def delete_task(id_task):
    user_id = get_jwt_identity()
    result = delete_task_id(user_id, id_task)
    if result:
        return {"message": "Task deleted successfully"}, 200
    else:
        return {"message": "Task not found"}, 404


'''
    - Creates a specific task, requires authentcation.
'''


@tasks_blueprint.route('/', methods=['POST'])
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
    filename = f"{video_id}.mp4"
    video_path = os.path.join(video_folder_path, filename)
    #video_folder_path = os.path.join('videos', filename)# Para que funcione en local windows

    # Ensure the directory exists
    os.makedirs(os.path.dirname(video_path), exist_ok=True)

    # Save the video
    try:
        video.save(video_path)
    except Exception as e:
        return {"error": str(e)}, 500

    # Generate timestamp
    timestamp = datetime.now()

    # The initial status of the video
    status = 'uploaded'

    # Save to data base
    stored_video = UploadVideo(video_uuid, filename, timestamp, status).execute()

    # Return confirmation message
    return jsonify({
        "message": "Video task was created successfully",
        "task": {
            "id": video_id,
            "timestamp": timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            "status": status
        }
    }), 200

