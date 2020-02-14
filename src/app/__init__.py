"""
    Initialise of app.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask import Flask
from .logging_config import create_logger

from .config import Config

APP = Flask(__name__)
APP.config.from_object(Config)
DB = SQLAlchemy(APP)
MIGRATE = Migrate(APP, DB, directory=APP.config['MIGRATION_DIR'])
MANAGER = Manager(APP)
MANAGER.add_command('db', MigrateCommand)
LOGGER = create_logger(APP.config['LOG_DIR'])

from .routers import main  # pylint: disable=wrong-import-position
from .models import *  # pylint: disable=wrong-import-position
