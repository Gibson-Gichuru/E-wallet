from tests import BaseTestConfig
from app.models import Status, User
from tests.settings import Settings


class TestUssidCallbackRoute(BaseTestConfig):

    def setUp(self) -> None:
        super().setUp()

        Status.register_actions()
            
    def test_unregistered_user_option(self):

        """
        Unregistered user phonenumber is given a register option once a session is created
        """
        expected_response = Settings.get_ussid_menu().get("welcome")

        response = self.client.post(
            Settings.ENDPOINT,
            data=Settings.make_request_body()
        )

        self.assertEqual(response.text,expected_response)

    def test_registered_user_response(self):

        """A registed user is shown the main menu"""

        user = Settings.create_user(active=True)

        user.add(user)

        menu = Settings.get_ussid_menu().get("main")

        response = self.client.post(
            Settings.ENDPOINT,
            data=Settings.make_request_body()
        )

        self.assertEqual(response.text, menu)


class TestAccountRegistation(BaseTestConfig):

    def setUp(self) -> None:
        super().setUp()

        Status.register_actions()

        self.menu = Settings.get_ussid_menu()

    def test_register_screen(self):

        """Show a new user Register Option"""

        menu = Settings.get_ussid_menu()

        response = self.client.post(
            Settings.ENDPOINT,
            data=Settings.make_request_body(text="1")
        )

        self.assertEqual(
            response.text,
            menu.get("register")
        )

    def test_client_terminates_session(self):

        """Session is terminated once the User selects cancel"""

        response = self.client.post(
            Settings.ENDPOINT,
            data=Settings.make_request_body(text="2")
        )

        self.assertEqual(
            response.text,
            self.menu.get("cancel")
        )

    def test_user_registration_sequence(self):

        """User Registration Sequence
            Assuming that the user has selected register as an option

        """
        response = self.client.post(
            Settings.ENDPOINT,
            data=Settings.make_request_body(text="1*testing")
        )

        user = User.query.filter_by(
            username="testing"
        ).first()

        self.assertEqual(response.text, self.menu.get("reg_success"))

        self.assertIsNotNone(user)

    def test_account_activation(self):

        user = Settings.create_user()

        user.add(user)

        response = self.client.post(
            Settings.ENDPOINT,
            data=Settings.make_request_body()
        )

        self.assertEqual(response.text, self.menu.get("activate"))

    def test_suspended_account_response(self):

        user = Settings.create_user(suspended=True)

        user.add(user)

        response = self.client.post(
            Settings.ENDPOINT,
            data=Settings.make_request_body()
        )

        self.assertEqual(response.text, self.menu.get("suspended"))

    def test_account_activation_accepted(self):

        user = Settings.create_user()

        user.add(user)

        response = self.client.post(
            Settings.ENDPOINT,
            data=Settings.make_request_body(text="1")
        )

        self.assertEqual(response.text, self.menu.get("activate_accept"))

    def test_account_activation_rejected(self):

        user = Settings.create_user()

        user.add(user)

        response = self.client.post(
            Settings.ENDPOINT,
            data=Settings.make_request_body(text="2")
        )

        self.assertEqual(response.text, self.menu.get("activate_reject"))

    def test_account_deactivaton(self):

        user = Settings.create_user(active=True)

        user.add(user)

        response = self.client.post(
            Settings.ENDPOINT,
            data=Settings.make_request_body(text="5")
        )

        updated_user = User.query.filter_by(
            username=user.username
        ).first()

        self.assertTrue(updated_user.account.status.default)

        self.assertEqual(
            response.text,
            self.menu.get("deactivate")
        )


class TransactionTests(BaseTestConfig):

    def setUp(self) -> None:
        super().setUp()

        Status.register_actions()

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
