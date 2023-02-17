from tests import BaseTestConfig
from tests.settings import Settings
from tests.task_setup import TaskTest


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

    def test_withdraw_complete_response(self):

        response = self.transact("2*100")

        self.assertEqual(
            response.text,
            self.menu.get("withdraw_success")
        )

    @TaskTest.task_wrapper(task_type="STATEMENT")
    def test_request_statement_response(self):

        response = self.transact(text="4")

        self.assertEqual(
            response.text,
            self.menu.get("statement")
        )

    @TaskTest.task_wrapper(task_type="BALANCE")
    def test_check_balance(self):

        balance = float(self.user.account.balance)

        response = self.transact("3")

        self.assertEqual(
            response.text,
            self.menu.get("check_balance") + "{}".format(
                balance
            )
        )

    @TaskTest.task_wrapper(task_type="TOPUP")
    def test_top_up_stk_push(self):

        """Top up request initiates an stk push task"""

        self.transact(text="1*100")
