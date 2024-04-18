from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

celery = Celery("tasks", broker="redis://redis:6379", backend="redis://redis:6379")
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

engine = create_engine("postgresql://postgres:password@db/videodatabase", echo=True)
Session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
