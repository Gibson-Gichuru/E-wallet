from flask import current_app
from app.models import Task
import functools


from app.decorators import update_task_state

@update_task_state
def update_balance_success(job, connection, result, *args, **kwargs):

    pass


