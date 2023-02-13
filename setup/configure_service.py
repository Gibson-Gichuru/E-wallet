import os
import subprocess
from config import base_dir
from . import logging, E_WALLET_SERVICE


def config_service(service_file):

    if os.path.exists(os.path.join(E_WALLET_SERVICE, service_file)):

        return

    logging.info("Service Not found installing")

    command = "sudo cp {} {}".format(
        os.path.join(base_dir, service_file),
        os.path.join(E_WALLET_SERVICE, service_file)
    )

    subprocess.run(command.split(),check=True)

    subprocess.run(
        "sudo systemctl daemon-reload".split()
    )

    subprocess.run(
        f"sudo systemctl start {service_file}".split()
    )

    subprocess.run(
        f"sudo systemctl enable {service_file}".split()
    )

    return True
