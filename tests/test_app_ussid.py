from tests import BaseTestConfig
from app.models import User
from tests.settings import Settings
from unittest import mock


class TestUssidCallbackRoute(BaseTestConfig):
     
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

    def test_unactivated_account_ussid_response(self):

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

    @mock.patch("app.ussid.views.top_up", autospec=True)
    @mock.patch("app.ussid.views.Task", autospec=True)
    def test_account_activation_accepted(self, task_mock, top_up):

        user = Settings.create_user()

        user.add(user)

        response = self.client.post(
            Settings.ENDPOINT,
            data=Settings.make_request_body(text="1")
        )

        self.assertEqual(response.text, self.menu.get("activate_accept"))

        task_mock.schedule.assert_called_with(
            owner=user,
            description="Account Activation",
            target_func=top_up,
            queue=self.app.queue,
            amount=self.app.config.get("ACTIVATION_AMOUNT"),
            phonenumber=user.phonenumber,
            metadata={'purpose': 'activation'}
        )

    def test_account_activation_rejected(self):

        user = Settings.create_user()

        user.add(user)

        response = self.client.post(
            Settings.ENDPOINT,
            data=Settings.make_request_body(text="2")
        )

        self.assertEqual(response.text, self.menu.get("activate_reject"))

    @mock.patch("app.ussid.views.User")
    def test_account_deactivaton(self, user_mock):

        fake_user = mock.Mock()

        user_mock.query.filter_by().first.return_value = fake_user

        user = Settings.create_user(active=True)

        user.add(user)

        response = self.client.post(
            Settings.ENDPOINT,
            data=Settings.make_request_body(text="5")
        )

        fake_user.account.deactivate.assert_called()

        self.assertEqual(
            response.text,
            self.menu.get("deactivate")
        )
