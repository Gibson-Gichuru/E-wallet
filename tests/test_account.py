from tests import BaseTestConfig
from app.models import User, Status, Actions


def create_user(account_default=True, account_status=None):

    user = User(username="test", phonenumber="254XXXX")

    if not account_default:

        account_status = Status.query.filter_by(
            status_name=account_status
        ).first()

        user.account.status = account_status

    return user


class TestAccount(BaseTestConfig):

    def setUp(self) -> None:
        super().setUp()

        Status.register_actions()

    def test_account_creation(self):

        """
        Account is Deactivated by default
        when a user is registered
        """

        user = create_user()

        user.add(user)

        self.assertEqual(
            user.account.status.status_name,
            "Deactivated"
        )

    def test_deactivated_account(self):

        """A deactivated account cannot transact"""

        user = create_user()

        self.assertFalse(user.account.can(Actions.TRANSACT))

    def test_suspended_account(self):

        """Suspended account can not perform any action"""

        user = create_user(account_default=False, account_status="Suspended")

        user.add(user)

        self.assertTrue(user.account.can(Actions.NOACTION))

        self.assertFalse(user.account.can(Actions.TRANSACT))
