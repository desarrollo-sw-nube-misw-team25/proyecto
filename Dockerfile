# Use an appropriate base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Create the videos directory and set permissions
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

# Set additional environment variables
ENV SQLALCHEMY_DATABASE_URI=postgresql://postgres:admin@34.136.103.218:5432/db
ENV GOOGLE_CREDENTIALS_PATH=/app/src/sw-nube-credentials.json
ENV CREDENTIALS_REQUEST=https://api.jsonbin.io/v3/b/663fa4e8e41b4d34e4f225cf
ENV JWT_SECRET_KEY=your-secret-key

# Expose the port that your app runs on
EXPOSE 5000

# Specify the command to run your application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.app:app"]
