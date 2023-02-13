#!/usr/bin/env python3
from setup.configure_nginx import configure_nginx
from setup.migrate_database import database_migrate
from setup.install_updates import install_updates
from setup.configure_service import config_service


if __name__ == "__main__":

    install_updates()
    database_migrate()
    config_service("e-wallet.service")
    config_service("e-wallet-worker.service")
    configure_nginx()
