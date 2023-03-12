import subprocess
from . import logging


def database_migrate():

    logging.info("Comparing database migration")

    command = "poetry run flask db {}"

    current_version = subprocess.run(
        command.format("current").split(),
        capture_output=True,
        encoding="utf-8"
    ).stdout.split()

    migration_schema_version = subprocess.run(
        command.format("heads").split(),
        capture_output=True,
        encoding="utf-8"
    ).stdout.split()

    if not current_version:

        subprocess.run(
            command.format("upgrade").split()
        )

    if current_version != migration_schema_version:

        logging.info("Running database migrations")

        subprocess.run(
            command.format("upgrade").split()
        )

    logging.info("Database uptodate")
