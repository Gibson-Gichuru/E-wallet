import subprocess
from setup import poetry_env


def install_updates():

    subprocess.run(
        "poetry install --no-root".split(),
        env=poetry_env,
        check=True
    )
