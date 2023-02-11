from .models import Payment, Account, Task
from sqlalchemy import event
from .job_callbacks import update_balance_success

@event.listens_for(Payment, "after_insert")
def update_account_balance(mapper, connection, target):

    job_owner = target.account.holder

    Task.schedule(
        owner=job_owner,
        description="Account balance update",
        target_func=Account.update_balance,
        on_success=update_balance_success,
        kwargs={
            "amount":target.amount,
            "account":job_owner.account
        }
    )