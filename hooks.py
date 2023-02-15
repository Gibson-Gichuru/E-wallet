#!/usr/bin/env python3
import os
import stat
from setup import logging
from config import base_dir
import argparse


def install_hooks():

    files = os.listdir(os.path.join(base_dir, "hooks"))

    file_permissions = (
        stat.S_IRUSR |
        stat.S_IWUSR |
        stat.S_IXUSR |
        stat.S_IRGRP |
        stat.S_IWGRP |
        stat.S_IXGRP
    )

    for file in files:

        symlink_path = os.path.join(base_dir, f".git/hooks/{file[:-3]}")

        file_path = os.path.join(base_dir, f"hooks/{file}")

        if os.path.islink(symlink_path):

            logging.info(f"{file}: Hook aready installed")

            continue
        
        os.chmod(file_path,file_permissions)

        os.symlink(file_path, symlink_path)

    logging.info("Hooks installed")


def uninstall_hooks():

    files = os.listdir(os.path.join(base_dir, ".git/hooks"))

    for file in files:

        path = os.path.join(base_dir, f".git/hooks/{file}")

        if os.path.islink(path):

            os.unlink(path)

            logging.info(f"Uninstalled {file}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="E-wallet repo git hooks installer",
        add_help=True
    )
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("-i", "--install", action="store_true")

    group.add_argument("-u", "--uninstall", action="store_true")

    args = parser.parse_args()

    if args.install:

        install_hooks()

    if args.uninstall:

        uninstall_hooks()
