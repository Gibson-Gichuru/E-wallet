from flask.views import MethodView
from flask import request, jsonify
from app.models import User, Payment
from datetime import datetime
from config import base_dir
import os
from os import remove


class StkCallback(MethodView):

    def delete_file(self, filename):

        try:
            remove(filename)

        except Exception as error:

            pass
        
    def handle_succes_checkout(self, data):

        with open(
            os.path.join(
                base_dir, "{}.checkout".format(
                    data.get("transactionId")
                )
            )
        ) as file:

            user_phone = file.readline()

        user = User.query.filter_by(
            phonenumber=user_phone
        ).first()

        amount = data.get("value").replace("KES", "")

        amount = amount.replace("'", "")

        payment = Payment(
            transaction_id=data.get("transactionId"),
            account=user.account,
            date=datetime.strptime(
                data.get("transactionDate"),
                "%Y%m%d%H%M%S"
            ),
            amount=float(amount)
        )

        payment.add(payment)

        Account.update_balance(
            transaction_type="CREDIT",
            holder=user,
            amount=int(float(amount))
        )

        metadata = data.get("requestMetadata")

        if metadata and metadata.get("purpose") == "activation":

            user.account.activate()
            
        self.delete_file(
            os.path.join(
                base_dir,
                "{}.checkout".format(
                    data.get("transactionId")
                )
            )
        )

    def handle_failed_checkout(self, data):

        self.delete_file(
            os.path.join(
                base_dir,
                "{}.checkout".format(
                    data.get("transactionId")
                )
            )
        )

    def post(self):

        request_data = request.get_json()

        payment_type = request_data.get("category")

        status = request_data.get("status")

        if payment_type == "MobileCheckout" and status == "Success":

            self.handle_succes_checkout(request_data)

            return jsonify({"message":"ok"})

        if payment_type == "MobileCheckout" and status == "Failed":

            self.delete_file(
                os.path.join(
                    base_dir,
                    "{}.checkout".format(
                        request_data.get("transactionId")
                    )
                )
            )

            return jsonify({"message":"ok"})
        
        # handle C2B payment

        user = User.query.filter_by(
            username=request_data.get("clientAccount")
        ).first()

        if user:

            payment = Payment(
                transaction_id=request_data.get("transactionId"),
                account=user.account,
                date=datetime.strptime(
                    request_data.get(""),
                    "%y%m%d%H%M%S"
                ),
                amount=request_data.get("value")
            )

            payment.add(payment)

        return jsonify({"message":"ok"})
