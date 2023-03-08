import os
import africastalking
from config import base_dir
from dotenv import load_dotenv


class AfriBase:

    load_dotenv(os.path.join(base_dir,".env"))

    USERNAME = os.environ.get("TALKING_USERNAME")

    KEY = os.environ.get("TALKING_API_KEY")

    def __init__(self) -> None:
        
        africastalking.initialize(
            username=AfriBase.USERNAME,
            api_key=AfriBase.KEY
        )
