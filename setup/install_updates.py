import subprocess


def install_updates():

    subprocess.run("poetry install".split())
