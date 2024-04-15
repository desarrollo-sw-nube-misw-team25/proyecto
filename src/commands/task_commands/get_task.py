from src.models.video_model import Video


def get_task_id(user_id, id_task):
    # Query the database for the task with the given ID
    task = Video.query.filter_by(id=id_task).first()

    if task is None:
        # No task found with that ID
        return None

    # Construct the download URL
    # TODO: Comparar si el path de hecho puede descargar
    download_url = f"/videos/{task.filename}"

    # Return a dictionary with the task's information
    return {
        'id': task.id_task,
        'filename': task.path,
        'timestamp': task.timestamp,
        'state': task.status,
        'download_url': download_url
    }