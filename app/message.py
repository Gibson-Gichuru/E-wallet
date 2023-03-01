import os
import africastalking
import json
from config import base_dir

try:

    africastalking.initialize(
        username=os.environ.get("TALKING_USERNAME"),
        api_key=os.environ.get("TALKING_API_KEY")
    )

except Exception as error:

    pass

SMS = africastalking.SMS


def get_templates():

    with open(os.path.join(base_dir, "sms_template.json")) as file:

        templates = json.load(file)

    return templates


def template_constructor(template_type, data):

    templates = get_templates()

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


def send_sms(tempate, recipients=(),**kwargs):

    sender = os.environ.get("TALKING_SHORT_CODE")

    sms_message = template_constructor(tempate,kwargs.get("data"))

    if not sms_message or not SMS:

        return

    SMS.send(sms_message,list(recipients),sender)
