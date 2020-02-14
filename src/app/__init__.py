"""
    Initialise of app.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask import Flask, Blueprint
from flask_restx import Api
from .logging_config import create_logger

from .config import Config

APP = Flask(__name__)
APP.config.from_object(Config)
DB = SQLAlchemy(APP)
MIGRATE = Migrate(APP, DB, directory=APP.config['MIGRATION_DIR'])
MANAGER = Manager(APP)
MANAGER.add_command('db', MigrateCommand)
LOGGER = create_logger(APP.config['LOG_DIR'])

BLUEPRINT = Blueprint('api', __name__, url_prefix='/api')
API = Api(
    app=BLUEPRINT,
    version="1.0",
    title="NgFg API",
    description="New generation Form generator API",
)
APP.register_blueprint(BLUEPRINT)


from .routers import main  # pylint: disable=wrong-import-position
from .models import *  # pylint: disable=wrong-import-position
