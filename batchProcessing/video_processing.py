from celery import Celery
import subprocess

#app = Celery('video_processing', backend='redis://localhost', broker='redis://localhost')

#app.task
def process_video(nombre_video):
    
    try:
        # Using docker-compose to run the batch-processing service with the video file as an argument
        subprocess.run([
            'docker-compose', 'run', '--rm', 
            'batch-processing', 
            f'/app/videos/{nombre_video}'
        ], check=True)
        return "Video processing complete"
    
    except subprocess.CalledProcessError as e:
        return f"Error processing video: {e}"

if __name__ == "__main__":
    
    result = process_video('864afb3e-88c1-407d-b2fd-92e65506cd18.mp4')
    print(result)