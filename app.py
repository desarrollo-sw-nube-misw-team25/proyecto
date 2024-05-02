from flask import Flask, request, jsonify
import errors
import subprocess
app = Flask(__name__)

@app.route("/procesarVideo/<video_id>", methods=["POST"])
def process_video(video_id):
   
    filename = f"{video_id}.mp4"
    command = f"sudo ./videoProcessing.sh  /mnt/nfs/general/unprocessed/{video_id}.mp4"
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
    
    return jsonify(response)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
