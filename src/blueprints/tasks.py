from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..commands.task_commands.create_task import create_task 
from ..commands.task_commands.get_all_tasks import get_all_tasks 
from ..commands.task_commands.get_task import get_task_id
from ..commands.task_commands.delete_task import delete_task_id 

tasks_blueprint = Blueprint('tasks', __name__, url_prefix='/api/tasks')


'''
    - Create a task, requires authentication. 
'''
@tasks_blueprint.route('',  methods=['POST'])
@jwt_required()
def post_task():
    data = request.json
    user_id = get_jwt_identity()
    task = create_task(user_id, data)
    return task, 201

'''
    - Geat all user tasks, requires authentication. 
'''
@tasks_blueprint.route('',  methods=['GET'])
@jwt_required()
def get_all_task():
    user_id = get_jwt_identity()
    tasks = get_all_tasks(user_id)
    return tasks, 200


'''
    - Get a specific task, requires authentcation.
'''
@tasks_blueprint.route('/<id_task>',  methods=['GET'])
@jwt_required()
def get_task(id_task):
    user_id = get_jwt_identity()
    task = get_task_id(user_id, id_task)
    if task:
        return task, 200
    else:
        return {"message": "Task not found"}, 404

'''
    - Delete a task, requires authentcation.
'''
@tasks_blueprint.route('/<id_task>',  methods=['DELETE'])
@jwt_required()
def delete_task(id_task):
    user_id = get_jwt_identity()
    result = delete_task_id(user_id, id_task)
    if result:
        return {"message": "Task deleted successfully"}, 200
    else:
        return {"message": "Task not found"}, 404