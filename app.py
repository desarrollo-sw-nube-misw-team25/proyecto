from flask import  jsonify
from google.cloud import pubsub_v1
import subprocess

project_id="sw-nube"
subscription_id="Video_data-sub"
subscriber=pubsub_v1.SubscriberClient()
subscription_path=subscriber.subscription_path(project_id,subscription_id)
#@app.route("/procesarVideo/<video_id>", methods=["POST"])
def process_video(video_id: pubsub_v1.subscriber.message.Message)->None:
   
    filename = f"{video_id}.mp4"
    command = f"./videoProcessing.sh  {filename}"
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        response = {
            'status': 'ok',
            'output': result.stdout.decode()
        }
    except subprocess.CalledProcessError as e:
        response = {
            'status': 'error',
            'error': e.stderr.decode()
        }
    video_id.ack()
    return jsonify(response)

streaming_pull_future=subscriber.subscribe(subscription_path,callback=process_video)

with subscriber:
    try:
        streaming_pull_future.result()
    except Exception:
        streaming_pull_future.cancel()
        streaming_pull_future.result()

