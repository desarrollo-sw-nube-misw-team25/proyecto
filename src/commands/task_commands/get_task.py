import os

from src.models.video_model import Video

processed_video_folder_path = "/mnt/nfs/general/processed"
def get_task_id(id_task):
    # Query the database for the task with the given ID
    video = Video.query.filter_by(id=id_task).first()

    if video is None:
        # No task found with that ID
        return None

    # Construct the download URL
    # TODO: Comparar si el path de hecho puede descargar
    download_url = os.path.join(processed_video_folder_path, video.filename)

    # Return a dictionary with the task's information
    return {
        'id': video.id,
        'filename': video.filename,
        'timestamp': video.timestamp,
        'state': video.status,
        'download_url': download_url
    }