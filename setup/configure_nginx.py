import os
import subprocess
from config import base_dir
from . import NGINX_SYMLINK_DIR, NGINX_CONFIG_DIR


def configure_nginx():

    # check if a simlink exists

    if os.path.islink(NGINX_SYMLINK_DIR):

        return False

    script_dir = os.path.join(base_dir, "configure_nginx.sh")

    copy_command = "{} {} {}"

    # constuct nginx config file

    subprocess.run(["bash", "-c", f"{script_dir}"], check=True)

    # copy the nginx config file

    subprocess.run(
        copy_command.format(
            "sudo cp",
            os.path.join(base_dir, "e-wallet.conf"),
            NGINX_CONFIG_DIR
        ).split(),
        check=True
    )

    # create a link

    subprocess.run(
        copy_command.format(
            "sudo ln -sf",
            "/etc/nginx/sites-available/e-wallet.conf",
            NGINX_SYMLINK_DIR
        ).split(),
        check=True
    )

    subprocess.run("sudo nginx -s reload".split(), check=True)

    return True
