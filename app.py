from google.cloud import pubsub_v1
import subprocess

timeout = 5.0
project_id="sw-nube"
subscription_id="Video_data-sub"
subscriber=pubsub_v1.SubscriberClient()
subscription_path=subscriber.subscription_path(project_id,subscription_id)

#@app.route("/procesarVideo/<video_id>", methods=["POST"])
def process_video(message: pubsub_v1.subscriber.message.Message)->None:
    video_id=message.data.decode("utf-8")
    print(video_id)
    filename = f"{video_id}.mp4"
    command = f"./videoProcessing.sh  {filename}"
    print(filename)
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
    except  Exception as e:
        raise(e)
    message.ack()
streaming_pull_future=subscriber.subscribe(subscription_path,callback=process_video)

with subscriber:
    try:
        streaming_pull_future.result()
    except Exception as e:
        streaming_pull_future.cancel()
        streaming_pull_future.result()
        raise(e)
