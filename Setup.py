#!/usr/bin/env python3
import subprocess
import sys
from setup.configure_nginx import  configure_nginx
from setup.migrate_database import database_migrate
from setup.install_updates import install_updates
from setup.launch_redis_worker import launch_redis_worker

from setup import logger


if __name__ == "__main__":

    install_updates()
    database_migrate()
    configure_nginx()
    launch_redis_worker()

    try:

        subprocess.run(
            "sudo systemctl reload-or-restart e-wallet".split(),
            check=True
        )

        logger.info("Service up and running")

    except subprocess.CalledProcessError as error:

        logger.error("Unable to deploy service")

        sys.exit()
