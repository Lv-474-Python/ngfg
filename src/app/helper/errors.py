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


class GroupNotExist(NotExist):
    """
    Group not exist exception
    """


class GroupUserNotExist(NotExist):
    """
    GroupUser not exist exception
    """


class NotSend(CustomException):
    """
    Base not send exception
    """


class ChoiceNotSend(NotSend):
    """
    Choice not send exception
    """


class NotEnoughOptionsSend(NotSend):
    """
    Choice not enough options send exception
    """


class SettingAutocompleteNotSend(NotSend):
    """
    Setting autocomplete not send exception
    """


class AlreadyExist(CustomException):
    """
    Already exist exception
    """


class FieldAlreadyExist(AlreadyExist):
    """
    Field exist exception
    """


class NotCreated(CustomException):
    """
    Base not created exception
    """


class NotDeleted(CustomException):
    """
    Base not deleted exception
    """


class GroupNotCreated(NotCreated):
    """
    Group not created exception
    """


class UserNotCreated(NotCreated):
    """
    User not created exception
    """


class GroupUserNotCreated(NotCreated):
    """
    Group user not created exception
    """


class GroupUserNotDeleted(NotDeleted):
    """
    Group user not deleted exception
    """


class GroupNameAlreadyExist(AlreadyExist):
    """
    Group name already exist exception
    """


class GroupUserAlreadyExist(AlreadyExist):
    """
    Group name already exist exception
    """


class ChoiceOptionNotCreated(NotCreated):
    """
    ChoiceOption not created exception
    """


class ChoiceOptionNotDeleted(NotDeleted):
    """
    ChoiceOption not deleted error
    """
