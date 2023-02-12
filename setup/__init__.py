import logging

logger = logging.basicConfig(
    level=logging.DEBUG,
    format="[:] %(process)d - %(levelname)s - %(message)s"
)

E_WALLET_SERVICE = "/etc/systemd/system/"

NGINX_SYMLINK_DIR = "/etc/nginx/sites-enabled/e-wallet.conf"

NGINX_CONFIG_DIR = "/etc/nginx/sites-available"