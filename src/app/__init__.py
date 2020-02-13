"""
    Initialise of app.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager
from flask_script import Manager
from flask import Flask

from oauthlib.oauth2 import WebApplicationClient

from .config import Config, GOOGLE_CLIENT_ID

APP = Flask(__name__)
APP.config.from_object(Config)
LOGIN_MANAGER = LoginManager()
LOGIN_MANAGER.init_app(APP)
DB = SQLAlchemy(APP)
MIGRATE = Migrate(APP, DB, directory=APP.config['MIGRATION_DIR'])
MANAGER = Manager(APP)
MANAGER.add_command('db', MigrateCommand)

GOOGLE_CLIENT = WebApplicationClient(GOOGLE_CLIENT_ID)

from .routers import main, auth  # pylint: disable=wrong-import-position
from .models import *  # pylint: disable=wrong-import-position
