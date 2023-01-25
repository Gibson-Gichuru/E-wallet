from tests import BaseTestConfig
import json


class TestUssidCallbackRoute(BaseTestConfig):

    def test_unregistered_user_option(self):

        """
        Unregistered user phonenumber is given a register option once a session is created
        """

        expected_response = "CON would you like \
             to regiser \n 1. Register Account \n 2. Cancel"

        response = self.client.post(
            "/ussid/callback",
            data=json.dumps(
                {
                    "session_id":"test1234",
                    "service_code":"166",
                    "phone_number":"254XXXXXXX",
                    "text":""
                }
            )
        )

        self.assertEqual(response.text,expected_response)
