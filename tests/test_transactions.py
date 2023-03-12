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

    @mock.patch("app.ussid.views.top_up", autospec=True)
    @mock.patch("app.ussid.views.Task", autospec=True)
    def test_top_up(self, task_mock, top_up_mock):

        """User top up option initiates stk push"""

        response = self.transact(text="1*100")

        task_mock.schedule.assert_called_with(

            owner=self.user,
            description="Topup Request",
            target_func=top_up_mock,
            queue=self.app.queue,
            amount=100,
            phonenumber=self.user.phonenumber
        )

        self.assertEqual(
            response.text,
            self.menu.get("topup_success")
        )

    @mock.patch("app.ussid.views.datetime", autospec=True)
    @mock.patch("app.ussid.views.send_sms", autospec=True)
    @mock.patch("app.ussid.views.Task", autospec=True)
    def test_balance(self, task_mock,msg_mock, date):

        """Balance request schedules a task"""

        date.utcnow.return_value = "test date"

        self.transact(text="3")

        data = {
            "balance":self.user.account.balance.to_eng_string(),
            "date":date.utcnow()
        }

        task_mock.schedule.assert_called_with(
            owner=self.user,
            description="Account Balance",
            target_func=msg_mock,
            queue=self.app.queue,
            template="BALANCE",
            data=data,
            recipient=f"+{self.user.phonenumber}"

        )

    @mock.patch("app.ussid.views.Task", autospec=True)
    def test_statement_request(self, task_mock):

        response = self.transact("4")

        records = self.user.account.generate_statement()

        task_mock.schedule.assert_called_with(
            owner=self.user,
            description="Account Statement",
            target_func=User.account_statement,
            queue=self.app.queue,
            records=records,
            cumulative_debit=self.user.account.cumulative_debit,
            cumulative_credit=self.user.account.cumulative_debit,
            balance=self.user.account.balance.to_eng_string(),
            recipient=f"+{self.user.phonenumber}"

        )

        self.assertEqual(
            response.text,
            self.menu.get("statement")
        )

    @mock.patch("app.ussid.views.User")
    @mock.patch("app.ussid.views.withdraw", autospec=True)
    @mock.patch("app.ussid.views.Task", autospec=True)
    def test_withdraw(self, task_mock, withdraw_mock, user_mock):

        fake_user = mock.Mock()

        fake_user.account.balance.to_eng_string.return_value = "1000.0"

        user_mock.query.filter_by().first.return_value = fake_user

        self.transact("2*100")

        task_mock.schedule.assert_called_with(
            owner=fake_user,
            description="Withdraw",
            target_func=withdraw_mock,
            queue=self.app.queue,
            name=fake_user.username,
            phonenumber=fake_user.phonenumber,
            amount=100
        )
