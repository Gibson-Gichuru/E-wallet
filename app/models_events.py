from .models import Payment, Account, Task
from sqlalchemy import event
from .job_callbacks import (
    update_balance_success,
)


@event.listens_for(Payment, "after_insert")
def update_account_balance(mapper, connection, target):

    Task.schedule(
        owner=target.account.holder,
        description="Account balance update",
        target_func=Account.update_balance,
        on_success=update_balance_success,
        amount=target.amount,
        holder=target.account.holder
    )


@event.listens_for(Account, "after_update")
def balance_notify(mapper, connection, target):

    # job_owner = target.holder

    # Task.schedule(
    #     owner=job_owner,
    #     description="Balance notification",
    #     target_func=Messanger.send_sms,
    #     on_success=success_notification
    # )

    pass

# @event.listens_for(User, "after_insert")
# def user_activation(mapper, connection, target):

#     # mpesa = Mpesa()

#     pass

#     # Task.schedule(
#     #     owner=target,
#     #     description="Account Activation",
#     #     target_func=Mpesa.stk_push,
#     #     on_success=success_notification,
#     #     amount=current_app.config["ACTIVATION_AMOUNT"],
#     #     phonenumber=target.phonenumber
#     # )
