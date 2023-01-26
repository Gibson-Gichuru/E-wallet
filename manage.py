import os
import sys
import json
from app import create_app
from app.models import User, Account, Task, Payment, Status, Actions
from werkzeug.exceptions import HTTPException

app = create_app(os.getenv("CONFIG") or "default")


@app.errorhandler(HTTPException)
def handle_exception(e):

    response = e.get_response()

    response.data = json.dumps({
        "code":e.code,
        "name":e.name,
        "description":e.description
    })

    response.content_type = "application/json"

    return response


@app.cli.command()
def test():

    import unittest

    tests = unittest.TestLoader().discover("tests")

    results = unittest.TextTestRunner(verbosity=2).run(tests)

    if not results.wasSuccessful():

        sys.exit()


@app.shell_context_processor
def shell_context():

    return dict(
        User=User,
        Account=Account,
        Actions=Actions,
        Payment=Payment,
        Status=Status,
        Task=Task
    )


@app.cli.command()
def migrate_db():

    from flask_migrate import upgrade

    upgrade()

    Status.register_actions()
