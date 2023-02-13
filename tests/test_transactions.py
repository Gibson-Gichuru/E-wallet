from tests import BaseTestConfig
from tests.settings import Settings


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
