#!/usr/bin/env python3
from config import base_dir
import subprocess
import os

test_command = "{} test"

def run_tests():

    subprocess.run(
        test_command.format(
            os.path.join(base_dir, "env/bin/flask")
        ),
        check=True
    )


if __name__ == "__main__":

    run_tests()