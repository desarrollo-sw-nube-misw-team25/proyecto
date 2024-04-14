from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from celery import Celery


from src.errors.errors import ApiError
from .blueprints.users import users_blueprint
from .blueprints.tasks import tasks_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videodatabase.db'  # Configure your database URI
app.config['REDIS_URI'] = 'redis://localhost'
app.config['BROKER_URI'] = 'redis://localhost'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional: disables modification tracking

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
celery = Celery('video_processing', backend=app.config['REDIS_URI'], broker=app.config['BROKER_URI'])
app.register_blueprint(users_blueprint)
app.register_blueprint(tasks_blueprint)

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
        "msg": err.description
    }
    return jsonify(response), err.code


if __name__ == '__main__':
    # Creates tables based on the models
    db.create_all()
    app.run(host='0.0.0.0')