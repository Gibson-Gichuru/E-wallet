from app.decorators import update_task_state


@update_task_state
def update_balance_success(job, connection, result, *args, **kwargs):

    pass


@update_task_state
def success_notification(job, connection, result, *args, **kwargs):

    pass


@update_task_state
def failed_stk_push(job, connection, result, *args, **kwargs):

    pass
