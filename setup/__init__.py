import logging
import os

poetry_env = os.environ.copy()

poetry_env_path = poetry_env.get("PATH").split(":")[0]

poetry_env['PATH'] = poetry_env_path + poetry_env['PATH']

logging.basicConfig(
    level=logging.DEBUG,
    format="[:] %(process)d - %(levelname)s - %(message)s"
)

E_WALLET_SERVICE = "/etc/systemd/system/"

NGINX_SYMLINK_DIR = "/etc/nginx/sites-enabled/e-wallet.conf"

NGINX_CONFIG_DIR = "/etc/nginx/sites-available"
