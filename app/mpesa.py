import requests 
from requests.exceptions import RequestException
from flask import current_app
from enum import Enum
import base64

class MpesaConsts(Enum):

    AUTH_URL="/oauth/v1/generate?grant_type=client_credentials"

    LNM_URL="/mpesa/stkpush/v1/processrequest"

class Mpesa:

    @staticmethod
    def encode(consumer_key, consumer_secret):

        token_encoded = f"{consumer_key}:{consumer_secret}".encode("utf-8")

        return base64.b64encode(token_encoded)

    def auth_tokens(self):

        auth_full_uri = "{}{}".format(
            current_app.config.get("MPESA_BASE_URL"),
            MpesaConsts.AUTH_URL
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
