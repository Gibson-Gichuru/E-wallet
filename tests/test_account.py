from tests import BaseTestConfig
from tests.settings import Settings
from app.models import Account
from unittest import mock, skip


class TestAccount(BaseTestConfig):

    def setUp(self):

        super().setUp()

        self.user = Settings.create_user(active=True)

        self.user.add(self.user)

    @mock.patch("app.models.Messanger", autospec=True)
    @mock.patch("app.models.Task.schedule", autospec=True)
    def test_balance_update_notification(self,schedule, msg):

        Account.update_balance(holder=self.user, amount=10)

        schedule.assert_called_with(
            owner=self.user,
            description="Balance Notification",
            target_func=msg.send_sms,
        )

    @skip("No implemented yet")
    @mock.patch("app.models.Messanger", autospec=True)
    @mock.patch("app.models.Task.schedule", autospec=True)
    def test_deactivation_update_notification(self, schedule, msg):

        self.user.account.deactivate()

        schedule.assert_called_with(
            owner=self.user,
            description="Account Status Change",
            target_func=msg.send_sms
        )
