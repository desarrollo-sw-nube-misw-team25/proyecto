import subprocess
import boto3
from flask import Flask, request

app = Flask(__name__)

# Initialize AWS SNS client
sns_client = boto3.client('sns', region_name='us-east-1b')

# Define the SNS topic ARN
sns_topic_arn = 'your-sns-topic-arn'

@app.route("/procesarVideo/<video_id>", methods=["POST"])
def process_video(video_id):
    print("Video processing starting [+]")
    filename = f"{video_id}.mp4"
    command = f"./videoProcessing.sh {filename}"
    print(filename)
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Video processing starting [+]")
        response = {
            'status': 'ok',
            'output': result.stdout.decode()
        }
        print(response)
    except subprocess.CalledProcessError as e:
        response = {
            'status': 'error',
            'error': e.stderr.decode()
        }
        print(response)
    except Exception as e:
        raise e

    return 'Video processing initiated.'

@app.route("/sns_endpoint", methods=["POST"])
def sns_endpoint():
    # Extract message from SNS notification
    sns_message = request.json
    video_id = sns_message.get('Message')

    # Process the video
    process_video(video_id)

    return 'Video processing initiated.'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
