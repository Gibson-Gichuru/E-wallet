import os
import subprocess
from config import base_dir
from . import NGINX_SYMLINK_DIR, NGINX_CONFIG_DIR

def configure_nginx():

    # check if a simlink exists

    if os.path.islink(NGINX_SYMLINK_DIR):

        return False

    construct_command = "envsubst < {} > {}".format(
        os.path.join(base_dir, "e-wallet.conf.template"),
        os.path.join(base_dir,"e-wallett.conf")
    )

    copy_command = "{} {} {}"

    # constuct nginx config file

    subprocess.run(construct_command.split(),check=True)

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
            "/etc/nginx/sites-available/e-wallet",
            NGINX_SYMLINK_DIR
        ),
        check=True
    )

    subprocess.run("sudo nginx -s reload".split(), check=True)

    return True
