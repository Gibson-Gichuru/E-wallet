import os


class Config:

    SECRETE_KEY = os.getenv("SECRETE_KEY")


class Development(Config):

    @staticmethod
    def init_app(app):

        pass 

class Testing(Config):

    TESTING = True 

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