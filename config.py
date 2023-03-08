import os
import logging

base_dir = os.path.abspath(os.path.dirname(__file__))
formatter = logging.Formatter("%(levelname)s :: %(message)s :: %(asctime)s")


def logger_setup(name, file, level=logging.INFO):

    handler = logging.FileHandler(file)

    handler.setFormatter(formatter)

    logger = logging.getLogger(name)

    logger.setLevel(level)

    logger.addHandler(handler)

    return logger


class Config:

    SECRETE_KEY = os.getenv("SECRETE_KEY")

    MPESA_BASE_URL = "https://sandbox.safaricom.co.ke"

    INITIATOR_NAME = os.environ.get("INITIATOR_NAME")

    INITIATOR_PASSWORD = os.environ.get("INITIATOR_PASSWORD")
     
    BUSINESS_SHORT_CODE = os.environ.get("BUSINESS_SHORT_CODE")

    PASS_KEY = os.environ.get("PASS_KEY")

    ACTIVATION_AMOUNT = os.environ.get("ACTIVATION_AMOUNT")

    @staticmethod
    def init_app(app):

        from app.models import Account

        from sqlalchemy import event

        def inject_app_obj(func):

            setattr(
                func,
                "_current_app",
                app
            )

            return func

        event.listen(
            Account.balance,
            "set",
            inject_app_obj(Account.balance_notify)
        )

        event.listen(
            Account.status_id,
            "set",
            inject_app_obj(Account.status_report_notify)
        )
        

class Development(Config):

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or \
        "sqlite:///" + os.path.join(base_dir, "dev-data.sqlite")

    MPESA_PHONENUMBER = os.environ.get("MPESA_PHONENUMBER")

    @staticmethod
    def init_app(app):

        Config.init_app(app=app)


class Testing(Config):

    TESTING = True

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or \
        "sqlite:///" + os.path.join(base_dir, "test-data.sqlite")

    MPESA_PHONENUMBER = os.environ.get("MPESA_PHONENUMBER")
    
    @staticmethod
    def init_app(app):

        Config.init_app(app=app)


class Production(Config):

    @staticmethod
    def init__app(app):

        Config.init_app(app=app)


config = {

    "default":Development,
    "development":Development,
    "testing":Testing,
    "production":Production
}
