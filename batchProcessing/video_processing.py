

from celery import Celery
import subprocess

app = Celery('video_processing', backend='redis://localhost', broker='redis://localhost')

@app.task
def process_video(video_path):
    
    try:    
        subprocess.run(['docker', 'run', '-v', f'{video_path}:/app/input', 'batch-processing', '/app/input/pruebaVideo.mp4'], check=True)
        return "Video processing complete"
    
    except subprocess.CalledProcessError as e:
        return f"Error processing video: {e}"

if __name__ == "__main__":
    
    result = process_video.delay('/home/pelucapreb/Descargas')
    print("Task ID:", result.id)




