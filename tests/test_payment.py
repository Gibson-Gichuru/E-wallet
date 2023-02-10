from tests import BaseTestConfig
from tests.settings import Settings
from unittest import mock
from app.models import Payment, Account
from datetime import datetime


class TestPayment(BaseTestConfig):

    def setUp(self):

        super().setUp()

        self.user = Settings.create_user(active=True)

        self.user.add(self.user)

        self.amount = 1

        self.payment = Payment(
            transaction_id="test",
            account=self.user.account,
            date=datetime.now(),
            amount=self.amount
        )

    @mock.patch("app.models_events.Task", autospec=True)
    def test_notification(self, task_mock):

        """User gets an SMS notification
            once a payment is done
        """

        pass
    
    @mock.patch("app.models_events.Task", autospec=True)
    @mock.patch("app.models_events.Account", autospec=True)
    def test_update_account_balance(self, payment_mock, task_mock):

        self.payment.add(self.payment)

        task_mock.schedule.assert_called_with(
            owner=self.payment.account.holder,
            description="Account balance update",
            target_func=payment_mock.update_balance,
            kwargs={
                "amount":self.amount,
                "account":self.payment.account
            }
        )




    