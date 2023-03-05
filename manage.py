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

        sys.exit(1)


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

    """Updating Database Schema"""

    from flask_migrate import upgrade

    upgrade()

    Status.register_actions()


@app.cli.command()
def stop_redis_worker():

    """Stop All Redis Workers"""

    from flask import current_app
    from rq.command import send_shutdown_command
    from rq.worker import Worker

    workers = Worker.all(current_app.redis)

    for worker in workers:

        send_shutdown_command(current_app.redis, worker.name)


@app.cli.command()
def tunnel():

    """Tunnel the application for callback testing"""

    from pyngrok import ngrok
    import logging
    from tempfile import mkstemp
    from shutil import move, copymode
    from os import fdopen, remove

    def update_env(file_path, pattern, replacement):

        temp_file, abs_path = mkstemp()

        with fdopen(temp_file, "w") as new_file:

            with open(file_path) as old_file:

                for line in old_file:

                    new_file.write(line.replace(pattern, replacement))

        copymode(file_path, abs_path)
        remove(file_path)
        move(abs_path,file_path)

    logging.basicConfig(level=logging.ERROR)

    try:

        print("starting the tunnel")

        https_tunnel = ngrok.connect(5000, "http", bind_tls=True)

        print(f"Base url:{https_tunnel.public_url}")

        file_path = os.path.abspath(os.path.dirname(".env"))

        urls = dict(
            stk_callback={
                "pattern":'STK_CALLBACK=""',
                "replacement":f"STK_CALLBACK={https_tunnel.public_url}/payment/stkcallback"
            },
            stk_notification={
                "pattern":'STK_NOTIFICATION=""',
                "replacement":f"STK_NOTIFICATION={https_tunnel.public_url}/payment/stknotification"
            },
            b2c_notification={
                "pattern":'B2C_NOTIFICATION=""',
                "replacement":f"B2C_NOTIFICATION={https_tunnel.public_url}/payment/b2cnotification"
            }
        )

        print("Updating env file")

        for url, item in urls.items():

            print(f"updating {url}")

            update_env(
                os.path.join(file_path, ".env"),
                item.get("pattern"),
                item.get("replacement")
            )

            print(f"{url} full url: {item.get('replacement')}")

        ngrok_process = ngrok.get_ngrok_process()

        ngrok_process.proc.wait()

    except KeyboardInterrupt:

        print("clossing the tunnel")

        map(
            lambda tunnel: ngrok.disconnect(tunnel.public_url),
            ngrok.get_tunnels()
        )

        print("Cleaning the env file")
        for url, item in urls.items():
            
            update_env(
                os.path.join(file_path, ".env"),
                item.get("replacement"),
                item.get("pattern"),
            )

        ngrok.kill()
