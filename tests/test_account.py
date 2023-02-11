from tests import BaseTestConfig
from tests.settings import Settings
from app.models import Account

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