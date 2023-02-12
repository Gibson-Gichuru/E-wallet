import os
import subprocess
from config import base_dir
from . import logger, E_WALLET_SERVICE

def config_service():

    if os.path.exists(os.path.join(E_WALLET_SERVICE, "e-wallet.service")):

        return

    logger.info("Service Not found installing")

    command = "sudo cp {} {}".format(
        os.path.join(base_dir,"e-wallet.service"),
        os.path.join(E_WALLET_SERVICE, "e-wallet.service")
    )


    subprocess.run(command.split(),check=True)

    subprocess.run(
        "sudo systemctl daemon-reload".split()
    )

    subprocess.run(
        "sudo systemctl enable e-wallet.service".split()
    )

    return True