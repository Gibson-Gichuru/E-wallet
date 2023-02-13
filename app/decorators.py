from app.models import Task
import functools


def update_task_state(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        if args:

            task = Task.query.filter_by(
                task_id=args[0].id
            ).first()

            task.complete = True

            task.update()

        return func(*args, **kwargs)
    
    return wrapper
