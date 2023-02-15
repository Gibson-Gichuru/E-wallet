#!/usr/bin/env python3
import logging
import subprocess
import os


logging.basicConfig(
    level=logging.DEBUG,
    format="[:] %(process)d - %(levelname)s - %(message)s"
)

base_dir = os.path.abspath(os.path.dirname("app"))

test_command = "{} test"


def run_tests():

    logging.info("Running Application tests")
    
    subprocess.run(
        test_command.format(
            os.path.join(base_dir, "env/bin/flask")
        ),
        check=True
    )


if __name__ == "__main__":

    run_tests()
