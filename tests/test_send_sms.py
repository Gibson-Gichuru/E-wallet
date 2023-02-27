from tests import BaseTestConfig
from unittest import mock
from app.message import send_sms
import os


class TestSendSMS(BaseTestConfig):

    def setUp(self) -> None:

        super().setUp()

        self.sender = os.environ.get("TALKING_SHORT_CODE")

    @mock.patch("app.message.template_constructor", autospec=True)
    @mock.patch("app.message.SMS", autospec=True)
    def test_send_sms(self, sms_mock,temp_mock):

        temp_mock.return_value = "testing"

        recipients = ("test",)
        
        send_sms("TESTING",recipients=recipients,data=None)

        sms_mock.send.assert_called_with(
            temp_mock("TEST",data=None),
            list(recipients),
            self.sender
        )
