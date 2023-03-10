from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from redis import Redis
from rq import Queue

conventions = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

meta_data = MetaData(naming_convention=conventions)

db = SQLAlchemy(metadata=meta_data)

migrate = Migrate()


def create_app(app_config: str) -> Flask:

    app = Flask(__name__)

    app.config.from_object(config[app_config])

    config[app_config].init_app(app)

    # register modules

    db.init_app(app=app)
    
    migrate.init_app(app=app, db=db)

    app.redis = Redis(unix_socket_path="/var/run/redis/redis-server.sock")

    app.queue = Queue("E-wallet", connection=app.redis)

    # register blueprints

    from app.ussid import ussid_blueprint

    from app.payments import payment_blueprint

    app.register_blueprint(ussid_blueprint, url_prefix="/ussid")

    app.register_blueprint(payment_blueprint, url_prefix="/payment")

    return app
