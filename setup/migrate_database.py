import os
import subprocess
from config import base_dir
from . import logger

def database_migrate():

    logger.info("Comparing database migration")

    flask_dir = os.path.join(base_dir, "env/bin/flask")

    command = "{} db {}"

    current_version = subprocess.run(
        command.format(flask_dir, "current").spit(),
        capture_output=True,
        encoding="utf-8"
    ).stdout.split()[0]

    migration_schema_version = subprocess.run(
        command.format(flask_dir, "heads").split(),
        capture_output=True,
        encoding="utf-8"
    ).stdout.split()[0]

    if current_version != migration_schema_version:

        logger.info("Running database migrations")

        subprocess.run(
            command.format(flask_dir, "upgrade").split()
        )

    logger.info("Database uptodate")

