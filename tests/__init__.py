import unittest

from app import create_app


class BaseTestConfig(unittest.TestCase):

    def setUp(self) -> None:
        
        self.app = create_app("testing")

        self.app_context = self.app.app_context()

        self.app_context.push()

        self.client = self.app.test_client()

    def tearDown(self) -> None:
        
        self.app_context.pop()

        self.app = None
