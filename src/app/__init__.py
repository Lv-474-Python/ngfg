"""
    Initialise of app.
"""

from flask import Flask
from .logging_config import create_logger


APP = Flask(__name__)
LOGGER = create_logger()

from .routers import main # pylint: disable=wrong-import-position
