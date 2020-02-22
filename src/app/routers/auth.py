"""
app to auth user by google services
"""
import os
import requests

from flask import redirect, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from app import APP, LOGIN_MANAGER, GOOGLE_CLIENT
from app.config import GOOGLE_PROVIDER_CONFIG
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


@APP.route('/login')
def login():
    """
    View for google login page

    :return:
    """
    if not current_user.is_authenticated:
        return GOOGLE_CLIENT.authorize(
            callback=url_for('callback', _external=True)
        )
    return redirect(url_for('index'))


@APP.route('/login/callback')
@GOOGLE_CLIENT.authorized_handler
def callback(response):
    """
    View for Google callback

    :param response: response from google auth server
    :return:
    """
    if response is None:
        return 'Access denied', 403

    userinfo = requests.get(
        GOOGLE_PROVIDER_CONFIG['userinfo_endpoint'],
        params={
            'access_token': response['access_token']
        }
    ).json()

    if userinfo.get('email_verified'):
        email = userinfo['email']
        username = userinfo['given_name']
        google_token = userinfo['sub']
    else:
        return "User email not available or not verified by Google", 400

    user = UserService.create(username=username, email=email, google_token=google_token)
    if user is not None:
        UserService.activate_user(user.id)
        login_user(user)

    return redirect(url_for('index'))


@login_required
@APP.route('/logout/')
def logout():
    """
    View for logout

    :return:
    """
    logout_user()
    return redirect(url_for('index'))
