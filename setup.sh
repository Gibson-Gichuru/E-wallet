#!/bin/bash

set -e

trap 'current_command=$BASH_COMMAND' DEBUG

trap 'echo "\"${current_command}\" command filed with exit code $?."' EXIT

PWD=$(pwd)

function deploy_update(){

    if [ -f "/etc/systemd/system/e-wallet.service" ]; then

        echo "Service file found"

        # installing updates

        install_updates

        sudo systemctl reload-or-restart e-wallet


    else

        echo "Setting up e-wallet service file"

        sudo cp $PWD/e-wallet.service "/etc/systemd/system"

        install_updates

        sudo systemctl daemon-reload

        sudo systemctl start e-wallet

        configure_nginx
    fi
}

function install_updates(){

    if [ ! -d $PWD/env ]; then

        python3 -m venv env 

    fi

    $PWD/env/bin/pip install -r $PWD/requirements.txt
}

function configure_nginx(){

    export SERVER_NAME=$(dig +short myip.opendns.com @resolver1.opendns.com)

    sudo envsubst < $PWD/e-wallet.conf.template > $PWD/e-wallet.conf

    sudo cp $PWD/e-wallet /etc/nginx/sites-available

    sudo ln -sf /etc/nginx/sites-available/e-wallet.conf /etc/nginx/sites-enabled

    sudo nginx -s reload
}

deploy_update