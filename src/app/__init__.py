"""
    Initialise of app.
"""

from flask import Flask


APP = Flask(__name__)


from .routers import main # pylint: disable=wrong-import-position
