import os
import africastalking
import json
from config import base_dir
from app.afri_config import AfriBase


class Messanger(AfriBase):

    SENDER = os.environ.get("TALKING_SHORT_CODE")

    def __init__(self) -> None:
        
        super().__init__()

        self.sms = africastalking.SMS

    def get_templates(self):

        with open(os.path.join(base_dir, "sms_template.json")) as file:

            templates = json.load(file)

        return templates

    def template_constructor(self, template_type, data):

        templates = self.get_templates()

        if template_type == "TOPUP":

            sms = lambda template, data: template.format(
                data.get("ref_no"),
                data.get("date"),
                data.get("amount"),
                data.get("balance")
            )

            return sms(template=templates.get("TOPUP"),data=data)

        if template_type == "BALANCE":

            sms = lambda template, data: template.format(
                data.get("balance"),
                data.get("date")
            )

            return sms(template=templates.get("BALANCE"), data=data)

        if template_type == "STATEMENT":

            sms = lambda template, data: template.format(
                data.get("date"),
                data.get("records_str"),
                data.get("cumulative_debit"),
                data.get("cumulative_credit"),
                data.get("balance")
            )
            return sms(template=templates.get("STATEMENT"), data=data)

        if template_type == "WITHDRAW":

            sms = lambda template, data: template.format(
                data.get("debited_amount"),
                data.get("ref_no"),
                data.get("balance")
            )

            return sms(template=templates.get("WITHDRAW"), data=data)

        if template_type == "CONFIRM":

            return templates.get("CONFIRM")

        if template_type == "ACTIVATE":

            return templates.get("ACTIVATE")
        
        if template_type == "DEACTIVATE":

            return templates.get("DEACTIVATE")

    def send_sms(self, template, **kwargs):

        data = kwargs.get("data")
        recp = kwargs.get("recipient")

        sms_message = self.template_constructor(
            template_type=template,
            data=data
        )

        self.sms.send(sms_message,[recp],Messanger.SENDER)


def send_sms(template, **kwargs):

    messanger = Messanger()

    messanger.send_sms(template=template, **kwargs)
