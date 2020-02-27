"""
Answer validation functions
"""


def is_numeric(value):
    """
    Functions to check whether value is numeric.

    :param value:
    :return: True if numeric, False else
    """
    try:
        float(value)
        return True
    except ValueError:
        return False
