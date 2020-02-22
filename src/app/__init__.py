"""
    Initialise of app.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager
from flask_script import Manager
from flask import Flask, Blueprint
from flask_restx import Api
from oauthlib.oauth2 import WebApplicationClient
from .logging_config import create_logger

from .config import Config, GOOGLE_CLIENT_ID

APP = Flask(__name__)
APP.config.from_object(Config)
LOGIN_MANAGER = LoginManager()
LOGIN_MANAGER.init_app(APP)
DB = SQLAlchemy(APP, session_options={'autocommit': True})
MIGRATE = Migrate(APP, DB, directory=APP.config['MIGRATION_DIR'])
MANAGER = Manager(APP)
MANAGER.add_command('db', MigrateCommand)
LOGGER = create_logger(APP.config['LOG_DIR'])

BLUEPRINT = Blueprint('api', __name__, url_prefix='/api/v1')
API = Api(
    app=BLUEPRINT,
    version="1.0",
    title="NgFg API",
    description="New generation Form generator API",
)
APP.register_blueprint(BLUEPRINT)

GOOGLE_CLIENT = WebApplicationClient(GOOGLE_CLIENT_ID)

from .routers import main, auth, field  # pylint: disable=wrong-import-position
from .models import *  # pylint: disable=wrong-import-position
