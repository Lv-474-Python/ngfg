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


class FieldRangeNotExist(NotExist):
    """
    FieldRange not exist exception
    """


class SharedFieldNotExist(NotExist):
    """
    SharedField not exist exception
    """

class UserNotExist(NotExist):
    """
    User not exist exception
    """


class SettingAutocompleteNotExist(NotExist):
    """
    SettingAutocomplete not exist exception
    """
