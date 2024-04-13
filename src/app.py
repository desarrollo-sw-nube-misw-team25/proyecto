from flask import Flask
from .blueprints.users import users_blueprint

app = Flask(__name__)
app.register_blueprint(users_blueprint)