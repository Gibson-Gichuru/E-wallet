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

        menu = Settings.get_ussid_menu()

        response = self.client.post(
            Settings.ENDPOINT,
            data=Settings.make_request_body(text="2")
        )

        self.assertEqual(
            response.text,
            menu.get("cancel")
        )

    def test_user_registration_sequence(self):

        """User Registration Sequence
            Assuming that the user has selected register as an option

        """
        menu = Settings.get_ussid_menu()

        response = self.client.post(
            Settings.ENDPOINT,
            data=Settings.make_request_body(text="testing")
        )

        user = User.query.filter_by(
            username="testing"
        ).first()

        self.assertEqual(response.text,menu.get("reg_success"))

        self.assertIsNotNone(user)
