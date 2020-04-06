"""
PyJWT library helper
"""

import jwt

from app.config import SECRET_KEY
from app.helper.constants import JWT_ALGORITHM, LEEWAY_TIME


def generate_token(payload):
    """
    Generate jwt token with given payload

    :param payload: token payload
    """
    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=JWT_ALGORITHM
    ).decode('utf-8')
    return token

def decode_token(token, verify=True):
    """
    Decode token

    :param token: token to decode
    :param verify: whether token should be verified with flags
    """
    data = jwt.decode(
        token,
        SECRET_KEY,
        leeway=LEEWAY_TIME,
        algorithms=[JWT_ALGORITHM],
        verify=verify
    )
    return data
