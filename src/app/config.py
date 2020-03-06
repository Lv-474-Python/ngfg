"""
    Configuration module for APP.
"""

import os
import requests

BASEDIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

DATABASE = {
    'POSTGRES_USER': os.environ.get('POSTGRES_USER'),
    'POSTGRES_PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
    'HOST': os.environ.get('HOST'),
    'PORT': os.environ.get('PORT'),
    'DB_NAME': os.environ.get('DB_NAME')
}

# Google auth configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
GOOGLE_PROVIDER_CONFIG = requests.get(GOOGLE_DISCOVERY_URL).json()


class Config:
    """
        A class to configurate APP from object.
    """
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DATABASE['POSTGRES_USER']}:"\
                              f"{DATABASE['POSTGRES_PASSWORD']}@" \
                              f"{DATABASE['HOST']}:{DATABASE['PORT']}/{DATABASE['DB_NAME']}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MIGRATION_DIR = os.path.join(BASEDIR, 'migrations')

    # Swagger
    SWAGGER_UI_DOC_EXPANSION = 'list'
    SWAGGER_UI_OPERATION_ID = True
    SWAGGER_UI_REQUEST_DURATION = True

    LOG_DIR = os.path.join(BASEDIR, 'logs')

    ERROR_404_HELP = False

    # celery
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')
    CELERY_DEFAULT_QUEUE = os.environ.get('CELERY_DEFAULT_QUEUE')

    # flask-mail
    MAIL_SERVER = 'smtp.gmail.com'
    SERVER_NAME = 'ngfg.com:8000'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
