#!/bin/sh

set -e
sleep 1m

celery -A app worker --loglevel=info -Q notification_queue,share_field_queue,share_form_to_group_queue,share_form_to_users_queue
