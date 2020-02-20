"""
Project decorators
"""

import functools
from sqlalchemy.exc import (
    IntegrityError,
    ProgrammingError,
    DataError)

from app import DB


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
        try:
            DB.session.begin(subtransactions=True)
            result = func(*args, **kwargs)
            DB.session.commit()
            return result
        except IntegrityError:
            DB.session.rollback()
            return None
        except ProgrammingError:
            DB.session.rollback()
            return None
        except DataError:
            DB.session.rollback()
            return None
    return wrapper
