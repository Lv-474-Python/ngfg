#!/bin/sh

set -e
sleep 1m
#until rabbitmqctl status -c '\q'; do
#  >&2 echo "Postgres is unavailable - sleeping"
#  sleep 1
#done

echo running

flask db upgrade

python run.py
