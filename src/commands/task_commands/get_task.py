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
    download_url = os.path.join(processed_video_folder_path, video.filename)

    # Return a dictionary with the task's information
    return {
        'id': video.id,
        'filename': video.filename,
        'timestamp': video.timestamp,
        'state': video.status,
        'download_url': download_url
    }


def get_video_task_id(id_task):
    # Query the database for the task with the given ID
    video = Video.query.filter_by(id=id_task).first()

    if video is None:
        # No task found with that ID
        return None

    # Construct the download URL
    download_url = video.download_url

    # Retrieve file from processed_video_folder_path and in the filename append _processed.mp4
    uncut_filename = video.filename.split(".")[0]
    download_url = os.path.join("app", "videos", "processed", uncut_filename + "_processed.mp4")

    # Return a dictionary with the task's information
    return download_url
