from tests import BaseTestConfig
from app.models import Actions
from tests.settings import Settings
from unittest import mock


class TestUser(BaseTestConfig):

    def test_user_creation(self):

        """
        Account is Deactivated by default
        when a user is registered
        """

        user = Settings.create_user()

        user.add(user)

        self.assertEqual(
            user.account.status.status_name,
            "Deactivated"
        )

    def test_deactivated_user_account(self):

        """A deactivated account cannot transact"""

        user = Settings.create_user()

        self.assertFalse(user.account.can(Actions.TRANSACT))

    def test_suspended_user_account(self):

        """Suspended account can not perform any action"""

        user = Settings.create_user(suspended=True)

        user.add(user)

        self.assertTrue(user.account.can(Actions.NOACTION))

        self.assertFalse(user.account.can(Actions.TRANSACT))

    @mock.patch("app.models_events.success_notification", autospec=True)
    @mock.patch("app.models_events.Task", autospec=True)
    @mock.patch("app.models_events.Mpesa", autospec=True)
    def test_account_activation_stk_push(self, mpesa_mock,task_mock, suc_mock):

        user = Settings.create_user()

        user.add(user)

        task_mock.schedule.assert_called_with(
            owner=user,
            description="Account Activation",
            target_func=mpesa_mock().stk_push,
            on_success=suc_mock,
            amount=self.app.config["ACTIVATION_AMOUNT"],
            phonenumber=user.phonenumber
        )
