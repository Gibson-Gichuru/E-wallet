from flask.views import MethodView
from flask import request
from config import base_dir
import os
import json
from app.models import User, Actions, Task
from app.mpesa import top_up, withdraw
from app.message import send_sms
from flask import current_app
from datetime import datetime


class UssidCallback(MethodView):

    def __init__(self) -> None:
        super().__init__()

        with open(os.path.join(base_dir,"ussid_response.json"), "r") as file:

            self.menu_text = json.load(file)

    def process_input(self, text):

        return (len(text.split("*")), text.split("*"))

    def process_level_1_menu_option_nill(self, user):

        if user:

            if user.account.status.default:

                return self.menu_text.get("activate")

            if user.account.can(Actions.TRANSACT):

                return self.menu_text.get("main")

            return self.menu_text.get("suspended")

        return self.menu_text.get("welcome")

    def process_level_1_menu_option_1(self, user):

        if user:

            if user.account.can(Actions.TRANSACT):

                return self.menu_text.get("top_up")

            Task.schedule(
                owner=user,
                description="Account Activation",
                target_func=top_up,
                queue=current_app.queue,
                amount=current_app.config.get("ACTIVATION_AMOUNT"),
                phonenumber=user.phonenumber,
                metadata={"purpose":"activation"}
            )

            return self.menu_text.get("activate_accept")

        return self.menu_text.get("register")

    def process_level_1_menu_option_2(self, user):

        if user:

            if user.account.can(Actions.TRANSACT):

                return self.menu_text.get("withdraw")

            return self.menu_text.get("activate_reject")

        return self.menu_text.get("cancel")

    def process_level_1_menu_option_3(self, user):

        balance = user.account.balance.to_eng_string()

        data = {
            "balance":balance,
            "date":datetime.utcnow()
        }

        Task.schedule(
            owner=user,
            description="Account Balance",
            target_func=send_sms,
            queue=current_app.queue,
            template="BALANCE",
            data=data,
            recipient=f"+{user.phonenumber}"
        )

        return self.menu_text.get(
            "check_balance"
        ) + "{}".format(balance)

    def process_level_1_menu_option_4(self, user):

        # Todo implement statement processing

        setattr(User.account_statement, "_current_app", current_app)

        records = user.account.generate_statement()

        Task.schedule(
            owner=user,
            description="Account Statement",
            target_func=User.account_statement,
            queue=current_app.queue,
            records=records,
            cumulative_debit=user.account.cumulative_debit,
            cumulative_credit=user.account.cumulative_credit,
            balance=user.account.balance.to_eng_string(),
            recipient=f"+{user.phonenumber}"
            
        )

        return self.menu_text.get("statement")

    def process_level_1_menu_option_5(self, user):

        user.account.deactivate()

        return self.menu_text.get("deactivate")

    def process_level_2_menu_option_nill(self,text, phone_number):

        user_name = text[-1][-1]

        new_user = User(
            username=user_name,
            phonenumber=phone_number.replace("+", "")
        )

        new_user.add(new_user)

        return self.menu_text.get("reg_success")

    def process_level_2_menu_option_1(self, user, amount):

        # Todo topup process

        if amount < 10:

            return self.menu_text.get("top_up_invalid")

        Task.schedule(
            owner=user,
            description="Topup Request",
            target_func=top_up,
            queue=current_app.queue,
            amount=amount,
            phonenumber=user.phonenumber
        )

        return self.menu_text.get("topup_success")

    def process_level_2_menu_option_2(self, user, amount):

        # Todo withdraw process

        if amount < 10 or amount >= int(
            float(user.account.balance.to_eng_string())
        ):

            return self.menu_text.get("withdraw_invalid_amount")
        
        Task.schedule(
            owner=user,
            description="Withdraw",
            target_func=withdraw,
            queue=current_app.queue,
            name=user.username,
            phonenumber=user.phonenumber,
            amount=amount
        )

        return self.menu_text.get("withdraw_success")

    def post(self):

        phone_number = request.values.get("phoneNumber", None)
        text = request.values.get("text", "default")

        user = User.query.filter_by(
            phonenumber=phone_number.replace("+", "")
        ).first()

        if self.process_input(text)[0] == 1:
            # First Menu
            if text == "":

                return self.process_level_1_menu_option_nill(user)

            elif text == "1":

                return self.process_level_1_menu_option_1(user)

            elif text == "2":

                return self.process_level_1_menu_option_2(user)

            elif text == "3":

                return self.process_level_1_menu_option_3(user)

            elif text == "4":

                return self.process_level_1_menu_option_4(user)

            elif text == "5":

                return self.process_level_1_menu_option_5(user)

            else:

                return self.menu_text.get("cancel")

        if self.process_input(text=text)[0] == 2:

            fine_text = self.process_input(text=text)

            if user is None:

                return self.process_level_2_menu_option_nill(
                    text=fine_text,
                    phone_number=phone_number
                )

            if user.account.can(Actions.TRANSACT):

                if fine_text[-1][0] == "1":

                    return self.process_level_2_menu_option_1(
                        user=user,
                        amount=int(fine_text[-1][-1])
                    )

                return self.process_level_2_menu_option_2(
                    user=user,
                    amount=int(fine_text[-1][-1])
                )

            return self.menu_text.get("cancel")

        return self.menu_text.get("invalid option")
