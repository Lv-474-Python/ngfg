"""
Token service
"""

from app import DB
from app.models import Token
from app.helper.decorators import transaction_decorator


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
