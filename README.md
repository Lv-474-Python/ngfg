# ngfg
## New Generation Form Generator


## Configuration

### Before you make your first migration, export the following environmental variables:
- POSTGRES_USER
- POSTGRES_PASSWORD
- HOST
- PORT
- DB_NAME

### Google auth

To add Google auth you need to export the following environmental variable:
 - GOOGLE_CLIENT_ID
 - GOOGLE_CLIENT_SECRET
 - APP_SECRET_KEY

And for http access export:
- OAUTHLIB_INSECURE_TRANSPORT="1"

### Install and configure rabbitmq-server on your machine:
* Install rabbitmq-server
```
sudo apt-get install rabbitmq-server
```
* Add user, vhost, set user tags and permissions
```
sudo rabbitmqctl add_user user password
sudo rabbitmqctl add_vhost vhost
sudo rabbitmqctl set_user_tags user administrator
sudo rabbitmqctl set_permissions -p vhost user ".*" ".*" ".*"
```
* Export the following environmental variables:
    + CELERY_BROKER_URL = "amqp://`your name`:`your password`@localhost/`your vhost`"
    + CELERY_RESULT_BACKEND = "rpc://"
    + CELERY_DEFAULT_QUEUE = "ngfg_queue"

    You can set custom CELERY_RESULT_BACKEND (Check out [Celery result backend documentation](https://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html#keeping-results))
