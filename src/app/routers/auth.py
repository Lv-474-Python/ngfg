import json
import os
import requests

from flask import redirect, request, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from app import APP, LOGIN_MANAGER, GOOGLE_CLIENT
from ..config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_DISCOVERY_URL
from ..models.users import User

APP.secret_key = os.urandom(24)


@LOGIN_MANAGER.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).first()


@APP.route('/home_page/')
def index():
    if current_user.is_authenticated:
        return (
            f"Hello, {current_user.username} <br>"
            "<a class='button' href='/logout'>Logout</a>"
        )

    return '<a class="button" href="/login">Google Login</a>'


def _get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@APP.route('/login')
def login():
    google_provider_cfg = _get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg['authorization_endpoint']

    request_uri = GOOGLE_CLIENT.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + '/callback',
        scope=['openid', 'email', 'profile']
    )

    return redirect(request_uri)


@APP.route('/login/callback')
def callback():
    code = request.args.get('code')

    google_provider_cfg = _get_google_provider_cfg()
    token_endpoint = google_provider_cfg['token_endpoint']

    token_url, headers, body = GOOGLE_CLIENT.prepare_token_request(
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

    GOOGLE_CLIENT.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg['userinfo_endpoint']
    uri, headers, body = GOOGLE_CLIENT.add_token(userinfo_endpoint)

    userinfo_response = requests.get(uri, headers=headers, data=body)

    userinfo = userinfo_response.json()

    if userinfo.get('email_verified'):
        google_token = userinfo['sub']
        email = userinfo['email']
        username = userinfo['given_name']
    else:
        return "User email not available or not verified by Google", 400

    if not User.query.filter(User.google_token == google_token).first():
        user = User.create(username=username, email=email, google_token=google_token)
    else:
        user = User.query.filter(User.google_token == google_token).first()

    login_user(user)

    return redirect(url_for("index"))


@APP.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
