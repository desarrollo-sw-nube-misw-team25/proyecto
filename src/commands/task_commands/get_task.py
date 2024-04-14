from src.models.video_model import Video


def get_task_id(user_id, id_task):
    # Query the database for the task with the given ID
    task = Video.query.filter_by(task_id=id_task, user_id=user_id).first()

    if task is None:
        # No task found with that ID
        return None

    # Construct the download URL
    download_url = f"/videos/{task.filename}"

    # Return a dictionary with the task's information
    return {
        'id': task.task_id,
        'state': task.state,
        'path': task.path,
        'download_url': download_url
    }