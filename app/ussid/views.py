from flask.views import MethodView
from flask import request
from config import base_dir
import os
import json
from app.models import User

class UssidCallback(MethodView):

    def __init__(self) -> None:
        super().__init__()

        with open(os.path.join(base_dir,"ussid_response.json"), "r") as file:

            self.menu_text = json.load(file)

    def post(self):

        session_id = request.values.get("sessionId", None)
        session_code = request.values.get("sessionCode", None)
        phone_number = request.values.get("phoneNumber", None)
        text = request.values.get("text", "default")

        user = User.query.filter_by(
            phonenumber=phone_number
        ).first()

        if user is None or user.account.status.status_name != "Active":

            # check if this is the start of the session

            if text == "":

                return self.menu_text.get("welcome")

            elif text == "1":

                return self.menu_text.get("register")

            elif text == "2":

                return self.menu_text.get("cancel")

            else:
                # validate user inputs
                user = User(username=text, phonenumber=phone_number)

                user.add(user)

                return self.menu_text.get("reg_success")

        else:

            return self.menu_text.get("main")
