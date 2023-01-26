from tests import BaseTestConfig
from app.models import Account, User, Status

class TestAccount(BaseTestConfig):

    def setUp(self) -> None:
        super().setUp()

        Status.register_actions()
        

    def test_account_creation(self):

        """
        Account is Deactivated by default 
        when a user is registered 
        """

        user = User(username="test", phonenumber="245XXXX")

        user.add(user)

        self.assertEqual(
            user.account.status.status_name,
            "Deactivated"
        )