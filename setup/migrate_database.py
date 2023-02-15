import os
import subprocess
from config import base_dir
from . import logging


def database_migrate():

    logging.info("Comparing database migration")

    flask_dir = os.path.join(base_dir, "env/bin/flask")

    command = "{} db {}"

    current_version = subprocess.run(
        command.format(flask_dir, "current").split(),
        capture_output=True,
        encoding="utf-8"
    ).stdout.split()

    migration_schema_version = subprocess.run(
        command.format(flask_dir, "heads").split(),
        capture_output=True,
        encoding="utf-8"
    ).stdout.split()

    if not current_version:

        subprocess.run(
            command.format(flask_dir, "upgrade").split()
        )

    if current_version != migration_schema_version:

        logging.info("Running database migrations")

        subprocess.run(
            command.format(flask_dir, "upgrade").split()
        )

    logging.info("Database uptodate")
