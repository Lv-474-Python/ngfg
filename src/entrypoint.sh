#!/bin/sh

set -e
sleep 1m

echo running

flask db upgrade

python run.py
