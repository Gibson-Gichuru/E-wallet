from tests import BaseTestConfig
from app.mpesa import Mpesa
from unittest import mock
from requests.exceptions import RequestException

class TestMpesaAuth(BaseTestConfig):

    def __init__(self):

        super().setUp()

        self.mpesa = Mpesa()

    @mock.patch("app.mpesa.base64",autospec=True) 
    def test_consumer_tokens_encoding(self, b64_mock):
        
        consumer_key = "some key"
        
        consumer_secret = "some secret"
        
        Mpesa.encode(consumer_key,consumer_secret)

        b64_mock.b64encode.assert_called_with(
            f"{consumer_key}:{consumer_secret}".encode("utf-8")
        )


    @mock.patch("app.mpesa.requests", autospec=True)
    def test_auth_token_called(self,request_mock):

        # assert that tokens were fetched
        auth_tokens = self.mpesa.auth_tokens()

        request_mock.get.assert_called()

    
    @mock.patch("app.mpesa.requests", autospec=True)
    def test_auth_token_exception_raised(self, request_mock):

        request_mock.get.side_effect = RequestException

        auth_tokens = self.mpesa.auth_tokens()

        self.assertIsNone(auth_tokens)

    @mock.patch("app.mpesa.requests", autospec=True)
    def test_valid_tokens_returned(self, request_mock):

        request_mock.get.return_value = {
            "access_token": "some token",
            "expires_in": "in the future"
        }

        auth_tokens = self.mpesa.auth_tokens()

        self.assertIsNotNone(auth_tokens)

