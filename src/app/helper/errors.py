"""
Custom exceptions
"""

class CustomException(Exception):
    """
    Base custom exception
    """

class NotExist(CustomException):
    """
    Base not exist exception
    """

class FieldNotExist(NotExist):
    """
    Field not exist exception
    """


class FormNotExist(NotExist):
    """
    Form not exist exception
    """
