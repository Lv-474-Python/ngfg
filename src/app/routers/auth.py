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
from flask_restx import Resource
from app import APP, GOOGLE_CLIENT, API
from app.config import GOOGLE_PROVIDER_CONFIG
from app.services import UserService

APP.secret_key = os.environ.get("APP_SECRET_KEY")

AUTH_NS = API.namespace('auth', "Auth APIs")


@AUTH_NS.route('/login/')
class LoginAPI(Resource):
    """
    Auth API

    url: 'auth/login/'
    methods: get
    """

    @API.doc(
        responses={
            302: 'Redirect to main page'
        }
    )
    # pylint: disable=no-self-use
    def get(self):
        """
        Doesn't work because Swagger doesn't support CORS requests
        """
        if not current_user.is_authenticated:
            return GOOGLE_CLIENT.authorize(
                callback=url_for('callback', _external=True)
            )
        return redirect(url_for('index'), code=302)


@AUTH_NS.route('/logout/')
class LogoutAPI(Resource):
    """
        Auth API

        url: 'auth/logout/'
        methods: get
        """

    @API.doc(
        responses={
            302: 'Redirect to main page',
            401: 'Unauthorized'   # pylint: disable=duplicate-code
        }
    )
    @login_required
    # pylint: disable=no-self-use
    def get(self):
        """
        Logout user
        """
        logout_user()
        return redirect(url_for('index'), code=302)


@APP.route('/home_page/')
def index():
    """
    Base page

    :return:
    """
    if current_user.is_authenticated:
        return (
            f"Hello, {current_user.username} <br>"
            "<a class='button' href='/api/v1/auth/logout/'>Logout</a>"
        )

    return '<a class="button" href="/api/v1/auth/login/">Google Login</a>'


@APP.route('/api/v1/auth/login/callback')
@GOOGLE_CLIENT.authorized_handler
def callback(response):
    """
    View for Google callback

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
