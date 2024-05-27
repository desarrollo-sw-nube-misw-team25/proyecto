
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
    && rm -rf /var/lib/apt/lists/*  

RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

RUN apt-get install -y apt-transport-https ca-certificates

RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

# Update the package list and install the Google Cloud SDK
RUN apt-get install -y google-cloud-sdk

RUN dos2unix /app/videoProcessing.sh && \
    chmod +x /app/videoProcessing.sh

EXPOSE 80

ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json

CMD ["python3", "app.py"]
