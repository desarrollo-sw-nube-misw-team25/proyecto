

from celery import Celery

# Create a Celery instance
app = Celery('video_processing', backend='redis://localhost', broker='redis://localhost')

# Define a Celery task
@app.task
def process_video(video_path):
    import subprocess
    
    try:
        # Run the Docker container to process the video
        subprocess.run(['docker', 'run', '-v', f'{video_path}:/app/input', 'batch-processing', '/app/input/pruebaVideo.mp4'], check=True)
        
        # Optionally, you can retrieve the processed video from the container or storage service
        # and return it or perform further processing.
        
        return "Video processing complete"
    except subprocess.CalledProcessError as e:
        # Handle errors
        return f"Error processing video: {e}"

if __name__ == "__main__":
    # Example usage:
    # Enqueue a task to process a video
    result = process_video.delay('/home/pelucapreb/Descargas')
    print("Task ID:", result.id)




