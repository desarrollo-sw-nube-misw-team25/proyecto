import os


from src.extensions import db,celery
import subprocess
from src.models.video_model import Video


@celery.task
def process_video(video_path):
    try:
        subprocess.run(['sudo', 'docker', 'run', '-v', f'{video_path}:/app/input', 'batch-processing',
                        '/app/input/pruebaVideo.mp4'], check=True)
        return "Video processing complete"

    except subprocess.CalledProcessError as e:
        return f"Error processing video: {e}"


@celery.task(name="create_task")
def create_task():
    # Query the database for all videos in the 'uploaded' state
    videos = Video.query.filter_by(state='uploaded').all()

    for video in videos:
        try:
            # Construct the paths
            video_filename = video.filename
            video_path = os.path.join('videos', video_filename)

            # Process the video with subprocess
            result = process_video.delay('videos')

            # Update the video state to 'processed'
            video.state = 'processed'
            db.session.commit()


        except subprocess.CalledProcessError as e:
            # Log the error
            print("System", f"Error processing video {video.id}: {e}")
            continue  # continue processing the next video

