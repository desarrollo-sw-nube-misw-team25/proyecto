# Use an appropriate base image
FROM python:3.8


# Set the working directory in the container
WORKDIR /app

COPY /batchProcessing/videoProcessing.sh /app/videoProcessing.sh

COPY /batchProcessing/idrl.jpg  /app/idrl.jpg

RUN chmod +x /app/videoProcessing.sh

RUN mkdir -p /app/videos

RUN chmod 777 /app/videos

# Copy the entire src directory into the container
COPY src/ /app/src/

# Copy the requirements.txt file into the container
COPY src/requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set PYTHONPATH environment variable
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Specify the command to run your application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.app:app"]
