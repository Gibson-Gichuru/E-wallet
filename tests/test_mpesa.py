from tests import BaseTestConfig
from unittest import mock
from app.mpesa import Payments, PaymentException, withdraw
from tests.settings import Settings
from config import base_dir
import json
import os


class TestMpesaAuth(BaseTestConfig):

    def setUp(self) -> None:

        super().setUp()

        self.payment = Payments()

        self.phonenumber = "test"
        self.amount = 1
        self.metadata = {"test":"test"}

    @mock.patch("app.mpesa.africastalking",autospec=True)
    def test_payment_object_config(self,afr_mock):

        afr_mock.initialize.assert_called

    @mock.patch("app.mpesa.africastalking", autospec=True)
    def test_invalid_amount(self, afr_mock):

        # test for invalid amount
        
        with self.assertRaises(ValueError):

            self.payment.checkout(
                phonenumber=self.phonenumber,
                amount=self.amount,
                metadata=self.metadata
            )

    @mock.patch("app.mpesa.NamedTemporaryFile", autospec=True)
    @mock.patch("app.mpesa.rename", autospec=True)
    @mock.patch("app.mpesa.africastalking", autospec=True)
    def test_success_payment_checkout(self, afr_mock, _, _2):

        afr_mock.Payment.mobile_checkout.return_value = {
            "status": "PendingConfirmation",
            "description": "test",
            "transactionId": "test",
            "providerChannel": "test",
        }
        
        # test for a success checkout

        self.payment.checkout("test", 10, self.metadata)

        afr_mock.Payment.mobile_checkout.assert_called_with(
            Payments.PRODUCTNAME,
            f"+{self.phonenumber}",
            Payments.CURRENCY_CODE,
            10,
            self.metadata
        )

        # test for a failed checkout
        
    @mock.patch("app.mpesa.africastalking", autospec=True)
    def test_failed_checkout(self, afri_mock):
        
        afri_mock.Payment.mobile_checkout.return_value = {
            "status": "InvalidRequest",
            "description": "testing",
        }

        with self.assertRaises(PaymentException):

            self.payment.checkout(
                phonenumber=self.phonenumber,
                amount=10,
                metadata=self.metadata
            )

    @mock.patch("app.mpesa.NamedTemporaryFile", autospec=True)
    @mock.patch("app.mpesa.rename", autospec=True)
    @mock.patch("app.mpesa.africastalking", autospec=True)
    def test_write_to_file(self, afri_mock, rename_mock, temp_mock):

        afri_mock.Payment.mobile_checkout.return_value = {
            "status": "PendingConfirmation",
            "description": "test",
            "transactionId": "test",
            "providerChannel": "test",
        }

        fake_file = mock.Mock()

        fake_file.name = "test"

        temp_mock.return_value.__enter__.return_value = fake_file

        self.payment.checkout("test", 10)

        fake_file.write.assert_called_with("test".encode('utf-8'))

        rename_mock.assert_called_with(fake_file.name, "test.checkout")


class TestSTKCheckout(BaseTestConfig):

    def setUp(self):

        super().setUp()

        self.success_checkout = Settings.checkout_response()

        self.failed_checkout = Settings.checkout_response(
            success=False
        )

    @mock.patch("app.payments.views.Account", autospec=True)
    @mock.patch("app.payments.views.datetime", autospec=True)
    @mock.patch("app.payments.views.remove", autospec=True)
    @mock.patch("app.payments.views.User")
    @mock.patch("app.payments.views.Payment", autospec=True)
    def test_success_transaction(self,payment_mock, user_mock, rm_mock, date_mk,acc_mock):

        payment_obj = mock.Mock()

        user_mock.query.filter_by.first.return_value = mock.Mock()
        
        user = user_mock.query.filter_by().first()
        
        payment_mock.return_value = payment_obj

        date_mk.strptime.return_value = "test"

        with mock.patch("app.payments.views.open",mock.mock_open(read_data="test")):

            amount = self.success_checkout.get("value").replace("KES", "")

            amount = amount.replace("'","").strip()

            self.client.post(
                Settings.STKCALLBACK,
                headers={"content-type": "application/json"},
                data=json.dumps(self.success_checkout),
            )
            # assert that a payment object has been created

            payment_mock.assert_called_with(
                transaction_id=self.success_checkout.get("transactionId"),
                account=user.account,
                date=date_mk.strptime(),
                amount=float(amount)
            )

            acc_mock.update_balance.assert_called_with(
                transaction_type="CREDIT",
                holder=user,
                amount=int(float(amount))
            )

            rm_mock.assert_called_with(
                os.path.join(
                    base_dir,
                    "{}.checkout".format(
                        self.success_checkout.get(
                            "transactionId"
                        )
                    )
                )
            )
        
    @mock.patch("app.payments.views.datetime", autospec=True)
    @mock.patch("app.payments.views.remove", autospec=True)
    @mock.patch("app.payments.views.User")
    @mock.patch("app.payments.views.Payment", autospec=True)
    def test_failed_transaction(self, p_mock, u_mock, rm_mock, dt_mock):

        dt_mock.strptime.return_value = "test"

        with mock.patch("app.payments.views.open", mock.mock_open(read_data="test")) as file:

            self.client.post(
                Settings.STKCALLBACK,
                headers={"content-type": "application/json"},
                data=json.dumps(self.failed_checkout),
            )

            p_mock.assert_not_called()

            rm_mock.assert_called_with(
                os.path.join(
                    base_dir,
                    "{}.checkout".format(
                        self.failed_checkout.get(
                            "transactionId"
                        )
                    )
                )
            )


class TestC2BTransaction(BaseTestConfig):

    def setUp(self):

        super().setUp()

        self.c2b_response = Settings.checkout_response(c2b=True)

    @mock.patch("app.payments.views.Account", autospec=True)
    @mock.patch("app.payments.views.datetime", autospec=True)
    @mock.patch("app.payments.views.User")
    @mock.patch("app.payments.views.Payment", autospec=True)
    def test_C2B_success_transaction(self, payment_mock, user_mock, date_mock, acc_mock):

        amount = self.c2b_response.get("value").replace("KES", "")

        amount = amount.replace("'","").strip()

        user_mock.query.filter_by().first.return_value = mock.Mock()

        date_mock.strptime.return_value = "test"

        user = user_mock.query.filter_by().first()

        self.client.post(
            Settings.STKCALLBACK,
            headers={"content-type": "application/json"},
            data=json.dumps(self.c2b_response),
        )

        payment_mock.assert_called_with(
            transaction_id=self.c2b_response.get("transactionId"),
            account=user.account,
            date=date_mock.strptime(),
            amount=float(amount)
        )

        acc_mock.update_balance.assert_called_with(
            transaction_type="CREDIT",
            holder=user,
            amount=int(float(amount))
        )

    @mock.patch("app.payments.views.datetime", autospec=True)
    @mock.patch("app.payments.views.User")
    @mock.patch("app.payments.views.Payment", autospec=True)
    def test_C2B_unexpected_payment(self,payment_mock, user_mock, date_mock):

        # test user not found

        user_mock.query.filter_by().first.return_value = None

        self.client.post(
            Settings.STKCALLBACK,
            headers={"content-type": "application/json"},
            data=json.dumps(self.c2b_response),
        )

        payment_mock.assert_not_called()


class TestB2C(BaseTestConfig):

    def setUp(self) -> None:
        super().setUp()

        self.payment = Payments()

        self.amount = 100

        self.phone_number = "test"

        self.name = "test"

        self.b2c_response = Settings.b2c_response()

    @mock.patch("app.mpesa.NamedTemporaryFile", autospec=True)
    @mock.patch("app.mpesa.rename")
    @mock.patch("app.mpesa.africastalking", autospec=True)
    @mock.patch("app.mpesa.Payments", autospec=True)
    def test_b2c(self, payment_mock, afri_mock, rename_mock, temp_mock):

        payment_mock.PRODUCTNAME = "test"

        payment_mock.CURRENCY_CODE = "test"

        afri_mock.Payment.mobile_b2c.return_value = self.b2c_response

        fake_file = mock.Mock()

        fake_file.name = "test"

        temp_mock.return_value.__enter__.return_value = fake_file

        resp = self.payment.b2c(
            name=self.name,
            phonenumber=self.phone_number,
            amount=self.amount
        )

        afri_mock.Payment.mobile_b2c.assert_called_with(
            payment_mock.PRODUCTNAME,
            [
                dict(
                    name=self.name,
                    phoneNumber=f"+{self.phone_number}",
                    currencyCode=payment_mock.CURRENCY_CODE,
                    amount=self.amount,
                    reason="BusinessPayment",
                    metadata={"purpose":"withdraw"}
                )
            ]
        )

        rename_mock.assert_called_with(
            fake_file.name,
            "{}.checkout".format(
                self.b2c_response.get("entries")[0].get("transactionId")
            )
        )

        self.assertEqual(resp, self.b2c_response)

    @mock.patch("app.mpesa.Payments", autospec=True)
    def test_withdraw(self, payment_mock):

        payment_mock().b2c.return_value = self.b2c_response

        withdraw(
            name=self.name,
            phonenumber=self.phone_number,
            amount=self.amount,
        )

        payment_mock.assert_called()

        payment_mock().b2c.assert_called_with(
            name=self.name,
            phonenumber=self.phone_number,
            amount=self.amount,
        )


class TestB2CValidation(BaseTestConfig):

    def setUp(self) -> None:

        super().setUp()

        self.validation_data = Settings.b2c_validation()

    @mock.patch("app.payments.views.remove", autospec=True)
    @mock.patch("app.payments.views.User")
    @mock.patch("app.payments.views.Account")
    @mock.patch("app.payments.views.Withdraw")
    def test_b2c_validation_success(self, withdraw_mock, account_mock, user_mock, rm_mock):

        fake_user = mock.Mock()

        fake_user.account.balance.to_eng_string.return_value = "1000.00"

        user_mock.query.filter_by().first.return_value = fake_user

        with mock.patch("app.payments.views.open", mock.mock_open(read_data="test")):

            response = self.client.post(
                Settings.B2CCALLBACK,
                headers={"content-type": "application/json"},
                data=json.dumps(self.validation_data),
            )

            withdraw_mock.assert_called_with(
                transaction_id=self.validation_data.get("transactionId"),
                account=fake_user.account,
                amount=self.validation_data.get("amount")
            )

            account_mock.update_balance.assert_called_with(
                "DEBIT",
                holder=fake_user,
                amount=self.validation_data.get("amount")
            )

            rm_mock.assert_called_with(
                os.path.join(
                    base_dir,
                    "{}.checkout".format(
                        self.validation_data.get(
                            "transactionId"
                        )
                    )
                )
            )

            self.assertEqual(
                response.get_json(),
                {"status": "Validated"}
            )

    @mock.patch("app.payments.views.Account")
    @mock.patch("app.payments.views.Withdraw")
    @mock.patch("app.payments.views.remove", autospec=True)
    @mock.patch("app.payments.views.User")
    def test_b2c_validation_failure(self,user_mock, rm_mock, *args, **kwargs):

        user_mock.query.filter_by().first.return_value = None

        with mock.patch("app.payments.views.open", mock.mock_open(read_data="test")):

            response = self.client.post(
                Settings.B2CCALLBACK,
                headers={"content-type": "application/json"},
                data=json.dumps(self.validation_data),
            )

            rm_mock.assert_called_with(
                os.path.join(
                    base_dir,
                    "{}.checkout".format(
                        self.validation_data.get(
                            "transactionId"
                        )
                    )
                )
            )

            self.assertEqual(response.get_json(),{"status": "Failed"})
