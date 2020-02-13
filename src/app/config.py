"""
    Configuration module for APP.
"""

import os

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


class Config:
    """
        A class to configurate APP from object.
    """
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DATABASE['POSTGRES_USER']}:" \
                              f"{DATABASE['POSTGRES_PASSWORD']}@" \
                              f"{DATABASE['HOST']}:{DATABASE['PORT']}/{DATABASE['DB_NAME']}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MIGRATION_DIR = os.path.join(BASEDIR, 'migrations')

    # Swagger
    SWAGGER_UI_DOC_EXPANSION = 'list'
    SWAGGER_UI_OPERATION_ID = True
    SWAGGER_UI_REQUEST_DURATION = True
