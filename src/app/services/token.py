"""
Token service
"""

from jwt import DecodeError

from app import DB, LOGGER
from app.models import Token
from app.helper.decorators import transaction_decorator
from app.helper.jwt_helper import decode_token
from app.schemas import TokenSchema


class TokenService:
    """
    Class for Token service
    """

    @staticmethod
    @transaction_decorator
    def create(token, form_id):
        """
        Create Token model

        :param token:
        :param form_id:
        :return: Token model object or None
        """
        tokens = TokenService.filter(token=token)
        if tokens:
            token = tokens[0]
            return token
        token = Token(token=token, form_id=form_id)
        DB.session.add(token)
        return token

    @staticmethod
    def get_by_id(token_id):
        """
        Get Token model by id

        :param token_id:
        :return: Token object or None
        """
        token = Token.query.get(token_id)
        return token

    @staticmethod
    def get_by_token(token):
        """
        Get Token object by token

        :param token:
        :return: Token object or None
        """

        token = Token.query.filter_by(token=token).first()
        return token

    @staticmethod
    def filter(token_id=None, token=None, form_id=None):
        """
        Token filter method

        :param token_id:
        :param token:
        :param form_id:
        :return: list of Token objects or empty list
        """
        filter_data = {}

        if token_id is not None:
            filter_data['id'] = token_id
        if token is not None:
            filter_data['token'] = token
        if form_id is not None:
            filter_data['form_id'] = form_id

        result = Token.query.filter_by(**filter_data).all()
        return result

    @staticmethod
    def decode_token_for_check(token):
        """
        Decode token for check

        :param token: token to decode
        """
        try:
            data = decode_token(token, verify=False)
            return data
        except DecodeError as ex:
            LOGGER.error('DecodeError, message: %s', ex.args)
            return None

    @staticmethod
    def validate_data(data):
        """
        Validate token data

        :param data: data to validate
        """
        errors = TokenSchema().validate(data)
        return (not bool(errors), errors)
