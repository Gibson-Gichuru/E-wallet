import os
from sqlalchemy import event

base_dir = os.path.abspath(os.path.dirname(__file__))


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

        from app.models import Account, Payment

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
            Payment,
            "after_insert",
            inject_app_obj(Payment.register_to_account)
        )


class Development(Config):

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or \
        "sqlite:///" + os.path.join(base_dir, "dev-data.sqlite")

    MPESA_PHONENUMBER = os.environ.get("MPESA_PHONENUMBER")

    ACTIVATION_AMOUNT = 1

    @staticmethod
    def init_app(app):

        Config.init_app(app=app)


class Testing(Config):

    TESTING = True

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or \
        "sqlite:///" + os.path.join(base_dir, "test-data.sqlite")

    MPESA_PHONENUMBER = os.environ.get("MPESA_PHONENUMBER")

    ACTIVATION_AMOUNT = 1
    
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
