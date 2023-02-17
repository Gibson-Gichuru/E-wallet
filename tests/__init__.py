import unittest
from app import create_app, db
from app.models import Status


class BaseTestConfig(unittest.TestCase):

    def setUp(self) -> None:
        
        self.app = create_app("testing")

        self.app_context = self.app.app_context()

        self.app_context.push()

        db.create_all()

        Status.register_actions()
        
        self.client = self.app.test_client()

    def tearDown(self) -> None:

        db.drop_all()
        
        self.app_context.pop()

        self.app = None

    def run(self, result=None):

        if not result.errors:

            super(BaseTestConfig, self).run(result)
