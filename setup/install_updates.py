import os
import subprocess
import sys
from config import base_dir
from . import logger

def install_updates():

    # check for python environment folder exits

    if not os.path.exists(os.path.join(base_dir, "env")):

        logger.info("Creating a virtual environment")

        subprocess.run(
            "python3 -m venv env".split(),
            check=True
        )

    # check if the dependency file exits

    if not os.path.exists(os.path.join(base_dir, "requirements.txt")):

        logger.error("Dependency file not found. Exiting")

        sys.exit(1)

    command = "{} install -r {}".format(
        os.path.join(base_dir, "env/bin/pip"),
        os.path.join(base_dir, "requirements.txt")
    )

    subprocess.run(command.spit(), check=True, timeout=90)