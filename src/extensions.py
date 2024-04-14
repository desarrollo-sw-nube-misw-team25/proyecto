from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from celery import Celery

celery = Celery(
    "video_processing", broker="redis://localhost", backend="redis://localhost"
)
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
