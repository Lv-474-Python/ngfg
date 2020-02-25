"""
Project decorators
"""

import functools
from sqlalchemy.exc import (
    IntegrityError,
    ProgrammingError,
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
        except IntegrityError:
            pass
        except ProgrammingError:
            pass
        except CustomException:
            pass
        DB.session.rollback()
        LOGGER.warning('something went wrong')
        return None
    return wrapper
