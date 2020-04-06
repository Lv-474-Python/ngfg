"""
    Initialise of app.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager
from flask_cors import CORS
from flask_script import Manager
from flask import Flask, Blueprint
from flask_restx import Api
from flask_marshmallow import Marshmallow
from flask_oauthlib.client import OAuth
from flask_mail import Mail
from flask_socketio import SocketIO

from redis import Redis
from .celery_config import make_celery
from .logging_config import create_logger
from .config import (
    Config,
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_PROVIDER_CONFIG,
    REDIS_PASSWORD
)

APP = Flask(__name__)
NGFG_CORS = CORS(
    APP,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=True,
    expose_headers=['session', "Set-Cookie"]
)
APP.config.from_object(Config)
REDIS = Redis(password=REDIS_PASSWORD)
LOGIN_MANAGER = LoginManager()
LOGIN_MANAGER.init_app(APP)
DB = SQLAlchemy(APP, session_options={'autocommit': True})
MIGRATE = Migrate(APP, DB, directory=APP.config['MIGRATION_DIR'])
MANAGER = Manager(APP)
MANAGER.add_command('db', MigrateCommand)
LOGGER = create_logger(APP.config['LOG_DIR'], filename='warning.log')
SHEET_LOGGER = create_logger(APP.config['LOG_DIR'], filename='sheet.log')
CONNECTIONS_LOGGER = create_logger(APP.config['LOG_DIR'], filename='connections.log')
MA = Marshmallow(APP)
BLUEPRINT = Blueprint('api', __name__, url_prefix='/api/v1')
API = Api(
    app=BLUEPRINT,
    version="1.0",
    title="NgFg API",
    description="New generation Form generator API",
)
APP.register_blueprint(BLUEPRINT)

CELERY = make_celery(APP)

GOOGLE_CLIENT = OAuth(APP).remote_app(
    'ngfg',
    base_url=GOOGLE_PROVIDER_CONFIG['issuer'],
    authorize_url=GOOGLE_PROVIDER_CONFIG['authorization_endpoint'],

    request_token_url=None,
    request_token_params={
        'scope': 'openid email profile',
    },

    access_token_url=GOOGLE_PROVIDER_CONFIG['token_endpoint'],
    access_token_method='POST',

    consumer_key=GOOGLE_CLIENT_ID,
    consumer_secret=GOOGLE_CLIENT_SECRET
)

MAIL = Mail(APP)

SOCKETIO = SocketIO(APP, cors_allowed_origins='*')

from .routers import (  # pylint: disable=wrong-import-position
    main,
    auth,
    form,
    field,
    user,
    group,
    form_field,
    form_answer,
    shared_field,
    shared_form,
    token
)
from .models import *  # pylint: disable=wrong-import-position
from .celery_tasks import *  # pylint: disable=wrong-import-position
