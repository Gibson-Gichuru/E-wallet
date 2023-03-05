import os
import json
from app.models import User, Status
from config import base_dir


class Settings:

    ENDPOINT = "/ussid/callback"
    STKCALLBACK = "/payment/stkcallback"

    @staticmethod
    def create_user(active=False, suspended=False):

        user = User(
            username="test",
            phonenumber=os.environ.get("PHONENUMBER","254XXXXXX")
        )

        if active:

            account_status = Status.query.filter_by(
                status_name="Active"
            ).first()

            user.account.status = account_status

        if suspended:

            account_status = Status.query.filter_by(
                status_name="Suspended"
            ).first()

            user.account.status = account_status

        return user

    @staticmethod
    def make_request_body(text=""):

        return {
            "sessionId":"test1234",
            "sessionCode":"test",
            "phoneNumber":os.environ.get("PHONENUMBER","254XXXXXX"),
            "text":text
        }

    @staticmethod
    def get_ussid_menu():

        with open(os.path.join(base_dir, "ussid_response.json"), "r") as file:

            menu = json.load(file)

        return menu

    @staticmethod
    def get_sms_templates():

        with open(os.path.join(base_dir, "sms_template.json"), "r") as file:

            templates = json.load(file)

        return templates

    @staticmethod
    def checkout_response(success=True, c2b=False):

        with open(os.path.join(base_dir, "tests/stk-response.json"), "r") as file:

            response = json.load(file)

        if not success:

            return response.get("failed")
        
        if c2b:

            return response.get("c2b_success")
        
        return response.get("success")
