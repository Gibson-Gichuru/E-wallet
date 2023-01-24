from tests import BaseTestConfig


class TestAppConfig(BaseTestConfig):

    def test_app_is_in_test_mode(self) -> None:

        self.assertTrue(self.app.config["TESTING"])
