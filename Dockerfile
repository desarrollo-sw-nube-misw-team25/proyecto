# Use an appropriate base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the entire src directory into the container
COPY src/ /app/src/

# Copy the requirements.txt file into the container
COPY src/requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set PYTHONPATH environment variable
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Specify the command to run your application
CMD ["python", "src/app.py"]
