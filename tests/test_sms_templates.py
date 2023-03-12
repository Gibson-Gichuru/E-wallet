from tests import BaseTestConfig
from app.message import Messanger
from tests.settings import Settings
import random
import string


class TestSMSTemplates(BaseTestConfig):

    def setUp(self):

        super().setUp()

        self.templates = Settings.get_sms_templates()

        self.messanger = Messanger()

    def test_top_up_sms_template(self):

        sms_data = {
            "ref_no":"test",
            "date":"test",
            "amount":"test",
            "balance":"test"
        }
        
        sms = self.messanger.template_constructor("TOPUP", data=sms_data)

        expected_template = lambda template, data: template.format(
            data.get("ref_no"),
            data.get("date"),
            data.get("amount"),
            data.get("balance")
        )

        self.assertEqual(
            sms,
            expected_template(
                template=self.templates.get("TOPUP"),
                data=sms_data
            )
        )

    def test_balance_sms_template(self):

        data = {"balance":"test", "date":"test"}

        sms = self.messanger.template_constructor("BALANCE", data=data)

        expected_template = lambda template, data: template.format(
            data.get("balance"),
            data.get("date")
        )

        self.assertEqual(
            sms,
            expected_template(
                self.templates.get("BALANCE"),
                data=data
            )
        )

    def test_static_sms_template(self):

        confirm_sms = self.messanger.template_constructor("CONFIRM", data=None)
        activate_sms = self.messanger.template_constructor("ACTIVATE", data=None)
        deactive_sms = self.messanger.template_constructor("DEACTIVATE", data=None)
        
        self.assertEqual(
            confirm_sms,
            self.templates.get("CONFIRM")
        )

        self.assertEqual(
            activate_sms,
            self.templates.get("ACTIVATE")
        )

        self.assertEqual(
            deactive_sms,
            self.templates.get("DEACTIVATE")
        )

    def test_statement_sms_template(self):

        test_records = [
            {
                "ref_no":random.choices(
                    string.ascii_uppercase + string.digits,
                    k=10
                ),
                "amount":random.randint(1,5),
                "date":"some random date"
            }
            for _ in range(5)
        ]

        string_rep = ""

        for record in test_records:

            string_rep += f"{record['ref_no']} {record['amount']} {record['date']}"

        data = dict(
            date="test",
            records_str=string_rep,
            cumulative_debit=20,
            balance=2
        )

        sms = self.messanger.template_constructor("STATEMENT", data=data)

        expected_template = lambda template, data: template.format(
            data.get("date"),
            data.get("records_str"),
            data.get("cumulative_debit"),
            data.get("cumulative_credit"),
            data.get("balance")
        )

        self.assertEqual(
            sms,
            expected_template(
                self.templates.get("STATEMENT"),
                data=data
            )
        )

    def test_withdraw_sms_template(self):

        data = dict(
            debited_amount=10,
            ref_no="rest",
            balance=20
        )

        sms = self.messanger.template_constructor("WITHDRAW", data=data)

        expected_tempate = lambda template, data: template.format(
            data.get("debited_amount"),
            data.get("ref_no"),
            data.get("balance")
        )

        self.assertEqual(
            sms,
            expected_tempate(
                self.templates.get("WITHDRAW"),
                data=data
            )
        )
