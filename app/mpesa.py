from os import rename
from config import base_dir
from tempfile import NamedTemporaryFile
import africastalking
from app.afri_config import AfriBase


class PaymentException(Exception):

    def __init__(self,message, status) -> None:

        super().__init__(f"status: {status}: description: {message}")


class Payments(AfriBase):

    PRODUCTNAME = "E-wallet"

    CURRENCY_CODE = "KES"

    def __init__(self) -> None:

        super().__init__()

        self.b2c_reason = "BusinessPayment"

        self.b2c_metadata = {"purpose":"withdraw"}

    def write_to_file(self, filename, content):

        with NamedTemporaryFile(delete=False, dir=base_dir) as file:

            file.write(content.encode('utf-8'))

            rename(
                file.name,
                "{}.checkout".format(
                    filename
                )
            )
        
    def checkout(self, phonenumber,amount, metadata={}):

        amount = int(amount)

        if amount < 10:

            raise ValueError("Invalid Amount")

        response = africastalking.Payment.mobile_checkout(
            Payments.PRODUCTNAME,
            f"+{phonenumber}",
            Payments.CURRENCY_CODE,
            amount,
            dict(metadata),
        )

        if response.get("status") == "PendingConfirmation":

            with NamedTemporaryFile(delete=False, dir=base_dir) as file:

                file.write(phonenumber.encode('utf-8'))

                rename(
                    file.name,
                    "{}.checkout".format(
                        response.get("transactionId")
                    )
                )
        
        else:

            raise PaymentException(
                response.get("description"),
                response.get("status")
            )


def top_up(phonenumber, amount, metadata={}):

    pay = Payments()

    pay.checkout(phonenumber, amount, metadata=metadata)
