
FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir google-cloud-pubsub

RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    lsb-release \
    ffmpeg \
    dos2unix \
    apt-transport-https \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Download and install the Google Cloud SDK
RUN curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-476.0.0-linux-x86_64.tar.gz \
    && tar -xf google-cloud-cli-476.0.0-linux-x86_64.tar.gz \
    && ./google-cloud-sdk/install.sh --quiet --additional-components kubectl

# Set path environment to include Google Cloud SDK binaries
ENV PATH $PATH:/app/google-cloud-sdk/bin

RUN dos2unix /app/videoProcessing.sh && \
    chmod +x /app/videoProcessing.sh

EXPOSE 8080

ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json

CMD ["python3", "app.py"]
