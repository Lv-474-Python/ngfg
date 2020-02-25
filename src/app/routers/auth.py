"""
app to auth user by google services
"""
import os
import requests

from flask import redirect, url_for, jsonify
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)
from flask_restx import Resource, fields
from werkzeug.exceptions import NotFound
from app import APP, GOOGLE_CLIENT, API
from app.config import GOOGLE_PROVIDER_CONFIG
from app.services import UserService

APP.secret_key = os.environ.get("APP_SECRET_KEY")

AUTH_NS = API.namespace('auth', 'Auth APIs')
MODEL = API.model('User', {
    'google_token': fields.String(required=True, description="User google token")
})


@AUTH_NS.route('/login/')
class LoginAPI(Resource):
    def get(self):
        if not current_user.is_authenticated:
            return GOOGLE_CLIENT.authorize(
                callback=url_for('callback', _external=True)
            )
        return redirect("/", code=302)


@AUTH_NS.route('/logout/')
class LogoutAPI(Resource):
    # @login_required
    def get(self):
        logout_user()
        return jsonify({
            'code': 200,
            'message': 'Unauthorized'
        })


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

    return jsonify(
        code=200
    )


@APP.route('/logout/')
# @login_required
def logout():
    """
    View for logout

    :return:
        """
    print(request.cookies.get('siss'))
    # logout_user()
    return redirect(url_for('index'))
