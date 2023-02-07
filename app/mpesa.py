import requests 
from requests.exceptions import RequestException
from flask import current_app
from enum import Enum
from datetime import datetime
import base64


class MpesaConsts(Enum):

    AUTH_URL="/oauth/v1/generate?grant_type=client_credentials"

    LNM_URL="/mpesa/stkpush/v1/processrequest"

    TIMESTAMP_FORMAT="%Y%m%d%H%M%S"

class Mpesa:

    @staticmethod
    def encode(consumer_key, consumer_secret):

        token_encoded = f"{consumer_key}:{consumer_secret}".encode("utf-8")

        return base64.b64encode(token_encoded)

    @staticmethod
    def lipa_na_mpesa_pass():

        timestamp = datetime.now().strftime(
            MpesaConsts.TIMESTAMP_FORMAT.value
        )

        full_string = "{}{}{}".format(
            current_app.config.get("BUSINESS_SHORT_CODE"),
            current_app.config.get("PASS_KEY"),
            timestamp
        )

        encoded_string = base64.b64encode(full_string.encode("utf-8"))

        return encoded_string 

    def auth_tokens(self):

        auth_full_uri = "{}{}".format(
            current_app.config.get("MPESA_BASE_URL"),
            MpesaConsts.AUTH_URL.value
        )

        encoded_tokens = Mpesa.encode(
            consumer_key= current_app.config.get("CONSUMER_KEY"),
            consumer_secret=current_app.config.get("CONSUMER_SECRET")
        )

        try:

            tokens = requests.get(
                auth_full_uri,
                headers = {'Authorization': f'Bearer {encoded_tokens}'}
            )

        except RequestException:

            return None

        return tokens
