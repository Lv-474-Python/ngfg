import functools
from sqlalchemy.exc import IntegrityError

from app import DB


def transaction_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # import pdb; pdb.set_trace()
            DB.session.begin(subtransactions=True)
            result = func(*args, **kwargs)
            DB.session.commit() # error is here
            return result
        except IntegrityError:
            DB.session.rollback()
            return None
    return wrapper
