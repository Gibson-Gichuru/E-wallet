import subprocess


def install_updates():

    subprocess.run(
        "poetry install --no-root".split(),
        shell=True,
        check=True
    )
