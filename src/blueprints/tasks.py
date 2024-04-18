from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.celery.celery_tasks import create_task, process_video
from ..commands.task_commands.get_all_tasks import get_all_tasks
from ..commands.task_commands.get_task import get_task_id
from ..commands.task_commands.delete_task import delete_task_id

tasks_blueprint = Blueprint("tasks", __name__, url_prefix="/api/tasks")
"""
    - Create a task, requires authentication. 
"""


@tasks_blueprint.route("/", methods=["POST"])
@jwt_required()
def post_task():
    video = request.files.get("video")
    user_id = get_jwt_identity()
    task = create_task(video, user_id)
    process_video.delay(task["id"])
    return jsonify(task), 201


"""
    - Geat all user tasks, requires authentication. 
"""


@tasks_blueprint.route("/", methods=["GET"])
@jwt_required()
def get_all_task():
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

    result = delete_task_id(id_task)
    return result
