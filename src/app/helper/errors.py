"""
Custom exceptions
"""
from werkzeug.exceptions import HTTPException


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


class FormFieldNotExist(NotExist):
    """
    FormField not exist exception
    """


class AnswerNotExist(NotExist):
    """
    Answer not exist exception
    """


class FormNotExist(NotExist):
    """
    Form not exist exception
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


class RangeNotExist(NotExist):
    """
    Range not exist exception
    """


class ChoiceOptionNotExist(NotExist):
    """
    ChoiceOption not exist exception
    """


class BadRequest(HTTPException):
    """
    Base bad request exception
    """
    def __init__(self, description):
        super().__init__()
        self.code = 400
        self.description = description


class Forbidden(HTTPException):
    """
    Base forbidden exception
    """
    def __init__(self, description):
        super().__init__()
        self.code = 403
        self.description = description


class NotFound(HTTPException):
    """
    Base not found exception
    """
    def __init__(self, description):
        super().__init__()
        self.code = 404
        self.description = description
