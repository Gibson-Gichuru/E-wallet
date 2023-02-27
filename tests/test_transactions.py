from tests import BaseTestConfig
from tests.settings import Settings
from unittest import mock
from app.models import User


class TransactionTests(BaseTestConfig):
    
    def setUp(self) -> None:
        super().setUp()

        self.menu = Settings.get_ussid_menu()

        self.user = Settings.create_user(active=True)

        self.user.add(self.user)

    def transact(self, text):

        return self.client.post(
            Settings.ENDPOINT,
            data=Settings.make_request_body(text=text)
        )

    @mock.patch("app.ussid.views.Mpesa", autospec=True)
    @mock.patch("app.ussid.views.Task", autospec=True)
    def test_top_up(self, task_mock, mpesa_mock):

        """User top up option initiates stk push"""

        response = self.transact(text="1*100")

        task_mock.schedule.assert_called_with(

            owner=self.user,
            description="Topup Request",
            target_func=mpesa_mock().stk_push,
            amount=100,
            phonenumber=self.user.phonenumber
        )

        self.assertEqual(
            response.text,
            self.menu.get("topup_success")
        )

    @mock.patch("app.ussid.views.send_sms", autospec=True)
    @mock.patch("app.ussid.views.Task", autospec=True)
    def test_balance(self, task_mock,msg_mock):

        """Balance request schedules a task"""

        self.transact(text="3")

        task_mock.schedule.assert_called_with(
            owner=self.user,
            description="Account Balance",
            target_func=msg_mock,
        )

    @mock.patch("app.ussid.views.Task", autospec=True)
    def test_statement_request(self, task_mock):

        response = self.transact("4")

        task_mock.schedule.assert_called_with(
            owner=self.user,
            description="Account Statement",
            target_func=User.account_statement,
            user=self.user

        )

        self.assertEqual(
            response.text,
            self.menu.get("statement")
        )
