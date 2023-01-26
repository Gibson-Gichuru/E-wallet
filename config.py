import os


base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:

    SECRETE_KEY = os.getenv("SECRETE_KEY")
     

class Development(Config):

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or \
    "sqlite:///" + os.path.join(base_dir, "dev-data.sqlite")

    @staticmethod
    def init_app(app):

        pass


class Testing(Config):

    TESTING = True

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or \
    "sqlite:///" + os.path.join(base_dir, "test-data.sqlite")

    @staticmethod
    def init_app(app):

        pass


class Production(Config):

    @staticmethod
    def init__app(app):

        pass


config = {

    "default":Development,
    "development":Development,
    "testing":Testing,
    "production":Production
}
