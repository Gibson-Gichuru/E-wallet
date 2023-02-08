from .models import Payment, Task
from sqlalchemy import event

@event.listens_for(Payment, "after_insert")
def user_notification_after_payment(mapper, connection, target):

    task_owner = target.account.holder

    Task.schedule(user=task_owner)
