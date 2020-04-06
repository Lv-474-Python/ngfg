#!/bin/sh

set -e

flask db upgrade

python run.py
#gunicorn -w 1 run:APP
