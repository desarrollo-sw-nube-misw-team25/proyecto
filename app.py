from google.cloud import pubsub_v1
from google.oauth2 import service_account
import subprocess
import requests


def fetch_credentials(url):
    response = requests.get(url)
    response.raise_for_status()  

timeout = 5.0
project_id="sw-nube"
subscription_id="Video_data-sub"
credentials_info = fetch_credentials('https://api.jsonbin.io/v3/b/663fa4e8e41b4d34e4f225cf')
credentials = service_account.Credentials.from_service_account_info(credentials_info)
subscriber = pubsub_v1.SubscriberClient(credentials=credentials)
subscription_path=subscriber.subscription_path(project_id,subscription_id)
#@app.route("/procesarVideo/<video_id>", methods=["POST"])
def process_video(message: pubsub_v1.subscriber.message.Message)->None:
    print("Video processing starting [+]")
    video_id=message.data.decode("utf-8")
    filename = f"{video_id}.mp4"
    command = f"./videoProcessing.sh  {filename}"
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
