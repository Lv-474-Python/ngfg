"""
app to auth user by google services
"""
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
from app.config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_DISCOVERY_URL
from app.services import UserService

APP.secret_key = os.environ.get("APP_SECRET_KEY")


@LOGIN_MANAGER.user_loader
def _load_user(user_id):
    """
    Load user from db by id. This method for LOGIN_MANAGER to handle session

    :param user_id:
    :return:
    """
    return UserService.get_by_id(user_id)


@APP.route('/home_page/')
def index():
    """
    Base page
    :return:
    """
    if current_user.is_authenticated:
        return (
            f"Hello, {current_user.username} <br>"
            "<a class='button' href='/logout'>Logout</a>"
        )

    return '<a class="button" href="/login">Google Login</a>'


def _get_google_provider_cfg():
    """
    return google config to authorization

    :return:
    """
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@APP.route('/login')
def login():
    """
    view for google login page
    :return:
    """
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
    """
    View for google callback

    :return:
    """
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

    user = UserService.create(username=username, email=email, google_token=google_token)

    login_user(user)

    return redirect(url_for("index"))


@APP.route('/logout/')
@login_required
def logout():
    """
    View for logout
    :return:
    """
    logout_user()
    return redirect(url_for('index'))
