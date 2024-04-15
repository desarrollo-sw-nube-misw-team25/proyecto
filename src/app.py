from flask import Flask, jsonify

from src.errors.errors import ApiError
from src.extensions import db, bcrypt, celery, jwt
from src.blueprints.users import users_blueprint
from src.blueprints.tasks import tasks_blueprint

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:password@db/videodatabase"
)

app.config["REDIS_URI"] = "redis://localhost:6379"
app.config["BROKER_URI"] = "redis://localhost"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = (
    False  # Optional: disables modification tracking
)
app.config["JWT_SECRET_KEY"] = "your-secret-key"  # Change this!

celery.conf.update(app.config)
celery.main = app.import_name
app.register_blueprint(users_blueprint)
app.register_blueprint(tasks_blueprint)


db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)


@app.errorhandler(ApiError)
def handle_exception(err):
    response = {"msg": err.description}
    return jsonify(response), err.code


if __name__ == "__main__":
    with app.app_context():
        # Creates tables based on the models
        db.create_all()
        app.run(host="0.0.0.0")
