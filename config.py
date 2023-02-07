import os


base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:

    SECRETE_KEY = os.getenv("SECRETE_KEY")

    MPESA_BASE_URL="https://sandbox.safaricom.co.ke"

    INITIATOR_NAME= os.environ.get("INITIATOR_NAME")

    INITIATOR_PASSWORD= os.environ.get("INITIATOR_PASSWORD")
     
    BUSINESS_SHORT_CODE = os.environ.get("BUSINESS_SHORT_CODE")

    PASS_KEY = os.environ.get("PASS_KEY")

class Development(Config):

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or \
        "sqlite:///" + os.path.join(base_dir, "dev-data.sqlite")

    MPESA_PHONENUMBER = os.environ.get("MPESA_PHONENUMBER")


    @staticmethod
    def init_app(app):

        pass


class Testing(Config):

    TESTING = True

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or \
        "sqlite:///" + os.path.join(base_dir, "test-data.sqlite")

    MPESA_PHONENUMBER = os.environ.get("MPESA_PHONENUMBER")

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
