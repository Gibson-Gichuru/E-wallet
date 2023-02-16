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

    def test_topup_complete_response(self):

        response = self.transact("1*100")

        self.assertEqual(
            response.text,
            self.menu.get("topup_success")
        )

    def test_withdraw_complete_response(self):

        response = self.transact("2*100")

        self.assertEqual(
            response.text,
            self.menu.get("withdraw_success")
        )

    def test_request_statement_response(self):

        response = self.transact(text="4")

        self.assertEqual(
            response.text,
            self.menu.get("statement")
        )

    def test_check_balance(self):

        balance = float(self.user.account.balance)

        response = self.transact("3")

        self.assertEqual(
            response.text,
            self.menu.get("check_balance") + "{}".format(
                balance
            )
        )

    @mock.patch("app.ussid.views.Task", autospec=True)
    @mock.patch("app.ussid.views.Mpesa", autospec=True)
    @mock.patch("app.ussid.views.success_notification", autospec=True)
    @mock.patch("app.ussid.views.failed_stk_push", autospec=True)
    def test_top_up_stk_push(
        self,
        failed_stk_mock,
        success_mock,
        mpesa_mock,
        task_mock
    ):

        """Top up request initiates an stk push task"""

        self.transact(text="1*100")

        task_mock.schedule.assert_called_with(
            owner=self.user,
            description="Topup Request",
            target_func=mpesa_mock().stk_push,
            on_success=success_mock,
            on_failure=failed_stk_mock,
            amount=100,
            phonenumber=self.user.phonenumber
        )
    
    @mock.patch("app.ussid.views.Task", autospec=True)
    @mock.patch("app.ussid.views.success_notification", autospec=True)
    @mock.patch("app.ussid.views.failed_notification", autospec=True)
    def test_statement_task_schedule(
        self,
        failed_mock,
        success_mock,
        task_mock,
    ):

        """Statement Task Schedule"""

        self.transact(text="4")

        task_mock.schedule.assert_called_with(
            owner=self.user,
            description="Account Statement",
            target_func=User.generate_statement,
            on_success=success_mock,
            on_failure=failed_mock,
            user=self.user
        )

    @mock.patch("app.ussid.views.Messanger", autospec=True)
    @mock.patch("app.ussid.views.failed_notification", autospec=True)
    @mock.patch("app.ussid.views.success_notification", autospec=True)
    @mock.patch("app.ussid.views.Task", autospec=True)
    def test_account_balance_task_schedule(
        self,
        task_mock,
        success_mock,
        failed_mock,
        messanger_mock
    ):

        """Balance Task Schedule"""

        self.transact("3")

        task_mock.schedule.assert_called_with(
            owner=self.user,
            description="Account Balance",
            target_func=messanger_mock.send_sms,
            on_success=success_mock,
            on_failure=failed_mock,
        )
