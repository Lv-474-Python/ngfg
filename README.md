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

### Google Sheets
User must share the sheet with ngfg-account@ngfg-268019.iam.gserviceaccount.com
or give link with editing permission

### Install and configure rabbitmq-server on your machine:
* Install rabbitmq-server
```
sudo apt-get install rabbitmq-server
```
* Add user, vhost, set user tags and permissions
```
sudo rabbitmqctl add_user username password
sudo rabbitmqctl add_vhost vhost
sudo rabbitmqctl set_user_tags usernamer administrator
sudo rabbitmqctl set_permissions -p vhost username ".*" ".*" ".*"
```
* Export the following environmental variables:
    + CELERY_BROKER_URL = "amqp://`your username`:`your password`@localhost/`your vhost`"
    + CELERY_RESULT_BACKEND = "rpc://"
    + CELERY_DEFAULT_QUEUE = "ngfg_queue"

    You can set custom CELERY_RESULT_BACKEND (Check out [Celery result backend documentation](https://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html#keeping-results))

### Install and configure redis-server on your machine:
* Install redis-server
```
sudo apt install redis-server
```
* Add user to redis-server
    + Open redis-conf file
    ```
     sudo nano /etc/redis/redis.conf
    ```
    + Find line at SECURITY section
    ```
    # requirepass foobared
    ```
    + Replace the previous line with the following line
    ```
    requirepass <your_password>
    ```
* Restart redis-server
```
sudo systemctl restart redis.service
```
* Export the following environmental variables:
    + REDIS_PASSWORD=<your_password