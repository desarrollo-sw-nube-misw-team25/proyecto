from datetime import datetime
import os
import subprocess
import uuid
from celery import Celery

from src.commands.task_commands.update_video import UpdateVideo
from src.commands.task_commands.upload_video import UploadVideo
from src.errors.errors import BadRequestApi, GeneralError

celery = Celery("tasks", broker="redis://redis:6379", backend="redis://redis:6379")


@celery.task()
def process_video(nombre_video):
    try:
        command = f"apt-get update && apt-get install -y ffmpeg dos2unix && chmod +x /app/videoProcessing.sh && /app/videoProcessing.sh /app/videos/unprocessed/{nombre_video}.mp4"
        subprocess.run(
            command,
            shell=True,  # Allows the use of shell syntax
            check=True,  # Raises CalledProcessError on non-zero exit status
            text=True,  # Ensures output/error are returned as strings
        )
        UpdateVideo(nombre_video, "processed").execute()
    except subprocess.CalledProcessError as e:
        UpdateVideo(nombre_video, "error").execute()
        raise GeneralError(f"Error processing video: {e}")


@celery.task(name="create_task")
def create_task(video, user_id):
    path = os.path.join("videos", "unprocessed")
    # Retrieve the video file from the request
    if not video:
        raise BadRequestApi("No video has been provided")

    # Generate a unique ID for the video and create the filename
    video_uuid = uuid.uuid4()
    video_id = str(video_uuid)
    filename = f"{video_id}.mp4"
    video_path = os.path.join(path, filename)

    os.makedirs(os.path.dirname(video_path), exist_ok=True)

    # Save the video
    try:
        video.save(video_path)
    except Exception as e:
        raise GeneralError(f"An error has ben ocurred: {e}")

    # Generate timestamp
    timestamp = datetime.now()

    # Save to data base
    UploadVideo(video_uuid, filename, timestamp, "uploaded", "").execute()
    return {
        "id": video_id,
        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "uploaded",
    }
