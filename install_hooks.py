#!/usr/bin/env python3
import os
from setup import logging
from config import base_dir


def install_hooks():

    files = os.listdir(os.path.join(base_dir, "hooks"))

    for file in files:

        if os.path.islink(os.path.join(base_dir, f".git/hooks/{file}")):

            logging.info(f"{file}: Hook aready installed")

            continue
        
        os.chmod(os.path.join(base_dir, f"hooks/{file}"),770)

        os.symlink(
            os.path.join(base_dir, f"hooks/{file}"),
            os.path.join(base_dir, f".git/hooks/{file}")
        )

        logging.info("Hooks installed")


if __name__ == "__main__":

    install_hooks()