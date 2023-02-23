from tests import BaseTestConfig
from tests.settings import Settings
from unittest import mock
from app.models import Payment
from datetime import datetime
from app.models import Account


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

    @mock.patch("app.models.Task.schedule", autospec=True)
    def test_update_account_balance(self, task_mock):

        self.payment.add(self.payment)

        task_mock.assert_called_with(
            owner=self.payment.account.holder,
            description="Account Balance update",
            target_func=Account.update_balance,
            amount=self.amount,
            holder=self.payment.account.holder
        )
