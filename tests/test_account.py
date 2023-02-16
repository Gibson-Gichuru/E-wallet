from tests import BaseTestConfig
from tests.settings import Settings
from app.models import Account
from unittest import mock


class TestAccount(BaseTestConfig):

    def setUp(self):

        super().setUp()

        self.user = Settings.create_user(active=True)

        self.user.add(self.user)

    def test_account_balance_update(self):

        initial_balance = self.user.account.balance

        Account.update_balance(
            account=self.user.account,
            amount=100
        )
        
        self.assertGreater(
            self.user.account.balance,
            initial_balance,
        )

    @mock.patch("app.models_events.success_notification", autospec=True)
    @mock.patch("app.models_events.Messanger", autospec=True)
    @mock.patch("app.models_events.Task", autospec=True)
    def test_notification_on_balance_update(self, task_mock, msg_mock, suc_mock):

        self.user.account.balance = 100

        self.user.account.update()

        task_mock.schedule.assert_called_with(
            owner=self.user,
            description="Balance notification",
            target_func=msg_mock.send_sms,
            on_success=suc_mock,
        )
