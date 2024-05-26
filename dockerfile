
FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir google-cloud-pubsub

RUN apt-get update && \
    apt-get install -y ffmpeg dos2unix && \
    rm -rf /var/lib/apt/lists/* # Clean up to reduce image size

RUN dos2unix /app/videoProcessing.sh && \
    chmod +x /app/videoProcessing.sh

EXPOSE 80

CMD ["python3", "app.py"]
