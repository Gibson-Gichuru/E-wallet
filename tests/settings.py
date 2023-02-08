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
    def stk_push_ack(success=True):

        response = {
            "MerchantRequestID": "test",
            "CheckoutRequestID": "test",
            "ResponseCode": "0",
            "ResponseDescription": "test",
            "CustomerMessage": "test"
        }

        if not success:

            response["ResponseCode"] = "1"

        return response
    
    @staticmethod
    def stk_callback_data(phonenumber, amount):

        with open(os.path.join(base_dir, "tests/stk-response.json"), "r") as file:

            data = json.load(file)

        items = data["Body"]["stkCallback"]["CallbackMetadata"]["Item"]

        MpesaReceiptNumber = items[1]["Value"]

        items[-1]["Value"] = phonenumber

        items[0]["Value"] = amount

        return data,MpesaReceiptNumber
