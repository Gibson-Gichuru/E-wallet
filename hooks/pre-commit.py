#!/usr/bin/env python3
from config import base_dir
import subprocess
from setup import logging
import sys
lint_command_one = f"flake8 {base_dir} " + \
"--count --select E9,F63,F7,F82 " + \
"--exclude __pycache__ --show-source --statistics"

lint_command_two = f"flake8 {base_dir} " + \
"--count --max-complexity=10" + \
" --max-line-length=100 " + \
"--ignore C901,E121,E221,E126,E231,E123,F841,W503,W293,W504 " + \
"--exclude __pycache__,migrations,env,hooks --show-source --statistics" 

def lint_code():

    logging.info("Linting the source code..")

    sys.exit()

    subprocess.run(lint_command_one.split(), check=True)

    subprocess.run(lint_command_two.split(), check=True)

if __name__ == "__main__":

    lint_code()