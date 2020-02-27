"""
Project decorators
"""

import functools
from sqlalchemy.exc import (
    IntegrityError,
    ProgrammingError,
    SQLAlchemyError
)

from app import DB, LOGGER
from .errors import CustomException


def transaction_decorator(func):
    """
    Transaction decorator

    :param func: function to decorate
    :return: function wrapper
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """
        Function decorator

        :param *args: args
        :param **kwargs: kwargs
        """
        DB.session.begin(subtransactions=True)
        try:
            result = func(*args, **kwargs)
            DB.session.commit()
            return result
        except IntegrityError as ex:
            LOGGER.error('IntegrityError, message: %s', ex.args)
        except ProgrammingError as ex:
            LOGGER.error('ProgrammingError, message: %s', ex.args)
        except CustomException as ex:
            LOGGER.error('CustomException, message: %s', ex.args)
        except SQLAlchemyError as ex:
            LOGGER.error('SQLAlchemyError, message: %s', ex.args)
        DB.session.rollback()
        return None
    return wrapper
