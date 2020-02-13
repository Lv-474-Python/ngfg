import os

BASEDIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

DATABASE = {
    'POSTGRES_USER': os.environ.get('POSTGRES_USER'),
    'POSTGRES_PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
    'HOST': os.environ.get('HOST'),
    'PORT': os.environ.get('PORT'),
    'DB_NAME': os.environ.get('DB_NAME')
}


class Config:
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DATABASE['POSTGRES_USER']}:{DATABASE['POSTGRES_PASSWORD']}@{DATABASE['HOST']}:{DATABASE['PORT']}/{DATABASE['DB_NAME']}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MIGRATION_DIR = os.path.join(BASEDIR, 'migrations')