import sqlite3

from app import APP
import json
import os

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

from flask import redirect, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user
)

from oauthlib.oauth2 import WebApplicationClient
import requests

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# from .db import init_db_command
# from .user import User

APP.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(APP)

# try:
#     init_db_command()
# except sqlite3.OperationalError:
#     # Assume it's already been created
#     pass

client = WebApplicationClient(GOOGLE_CLIENT_ID)


# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)


@APP.route('/home_page/')
def index():
    if current_user.is_authenticated:
        return (
            f"Hello, {current_user.name} <br>"
            "<a class='button' href='/logout'>Logout</a>"
        )
    else:
        return '<a class="button" href="/login">Google Login</a>'


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@APP.route('/login')
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg['authorization_endpoint']

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + '/callback',
        scope=['openid', 'email', 'profile']
    )

    return redirect(request_uri)


@APP.route('/login/callback')
def callback():
    code = request.args.get('code')

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg['token_endpoint']

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg['userinfo_endpoint']
    uri, headers, body = client.add_token(userinfo_endpoint)

    userinfo_response = requests.get(uri, headers=headers, data=body)

    userinfo = userinfo_response.json()

    if userinfo.get('email_verified'):
        token = userinfo['sub']
        email = userinfo['email']
        username = userinfo['given_name']
    else:
        return "User email not available or not verified by Google", 400

    # user = User(id_=token, name=username, email=email)
    #
    # # Doesn't exist? Add it to the database.
    # if not User.get(token):
    #     User.create(token, username, email)
    #
    # login_user(user)
    #
    # return redirect(url_for("index"))


@APP.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
