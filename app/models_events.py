from flask import current_app
from .models import Payment, Account, Task, User
from sqlalchemy import event
from .job_callbacks import (
    update_balance_success,
    success_notification
)
from app.mpesa import Mpesa
from app.message import Messanger


@event.listens_for(Payment, "after_insert")
def update_account_balance(mapper, connection, target):

    job_owner = target.account.holder

    Task.schedule(
        owner=job_owner,
        description="Account balance update",
        target_func=Account.update_balance,
        on_success=update_balance_success,
        amount=target.amount,
        account=job_owner.account
    )


@event.listens_for(Account, "after_update")
def balance_notify(mapper, connection, target):

    job_owner = target.holder

    Task.schedule(
        owner=job_owner,
        description="Balance notification",
        target_func=Messanger.send_sms,
        on_success=success_notification
    )


@event.listens_for(User, "after_insert")
def user_activation(mapper, connection, target):

    mpesa = Mpesa()

    Task.schedule(
        owner=target,
        description="Account Activation",
        target_func=mpesa.stk_push,
        on_success=success_notification,
        amount=current_app.config["ACTIVATION_AMOUNT"],
        phonenumber=target.phonenumber
    )
