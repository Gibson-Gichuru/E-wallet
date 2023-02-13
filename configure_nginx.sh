#!/bin/bash

envsubst < $PWD/e-wallet.conf.template > e-wallet.conf

sudo cp $PWD/e-wallet.conf /etc/nginx/sites-available

sudo ln -sf /etc/nginx/sites-available/e-wallet.conf /etc/nginx/sites-enabled

sudo nginx -s reload


