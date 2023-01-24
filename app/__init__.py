from flask import Flask
from config import config

def create_app(app_config: str) -> Flask:

    app = Flask(__name__)

    app.config.from_object(config[app_config])

    config[app_config].init_app(app)


    return app