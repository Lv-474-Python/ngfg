#!/bin/sh

set -e
sleep 1m
#while ! nc -w 1 $host $port 2>/dev/null
#do
#  echo -n .
#  sleep 1
#done

#until timeout 1 sh -c "cat < /dev/null > /dev/tcp/rabbitmq/5672"; do
#  >&2 echo "Rabbit MQ not up yet on rabbitmq"
#  sleep 5
#done

#echo "Rabbit MQ is up"

celery -A app worker --loglevel=info -Q notification_queue,share_field_queue,share_form_to_group_queue,share_form_to_users_queue
