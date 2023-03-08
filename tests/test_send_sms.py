from tests import BaseTestConfig
from unittest import mock
from app.message import send_sms, Messanger
import os


class TestSendSMS(BaseTestConfig):

    def setUp(self) -> None:

        super().setUp()

        self.messanger = Messanger()

        self.sender = os.environ.get("TALKING_SHORT_CODE")

    @mock.patch("app.message.Messanger", autospec=True)
    def test_send_sms_interface(self,messanger_mock):

        messanger_mock.template_constructor.return_value = "testing"

        recipient = "test"
        
        send_sms(
            template="TESTING",
            recipient=recipient,
            data=None
        )

        messanger_mock.assert_called()

        messanger_mock().send_sms.assert_called_with(
            template="TESTING",
            recipient=recipient,
            data=None
        )
