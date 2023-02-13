from flask.views import MethodView
from flask import request, jsonify, abort
from app.models import User, Payment
from flask import current_app
from datetime import datetime
from app.mpesa import MpesaConsts


class StkCallback(MethodView):

    def post(self):

        request_data = request.get_json()

        if not request_data:

            abort(400)

        checkout_id = request_data["Body"]["stkCallback"]["CheckoutRequestID"]

        payment_info = request_data["Body"]["stkCallback"]["CallbackMetadata"]["Item"]

        phone_number = current_app.redis.get(checkout_id).decode("utf-8")

        user = User.query.filter_by(phonenumber=phone_number).first()

        timestamp = datetime.strptime(
            str(payment_info[3]["Value"]),
            MpesaConsts.TIMESTAMP_FORMAT.value
        )

        payment = Payment(
            transaction_id=payment_info[1]["Value"],
            account=user.account,
            date=timestamp,
            amount=payment_info[0]["Value"]
        )

        payment.add(payment)

        return jsonify({"message":"ok"})
