"""
Range validator
"""
from app.helper.constants import MAX_TEXT_LENGTH


def validate_range_text(range_min, range_max):
    """
    Validates text range (from 0 to 255)
    :param range_min:
    :param range_max:
    :return:
    """
    errors = validate_range_checkbox(range_min=range_min, range_max=range_max)
    if range_min and range_min > MAX_TEXT_LENGTH:
        errors.append('Min range must\'t be greater than 255')
    if range_max and range_max > MAX_TEXT_LENGTH:
        errors.append('Max range must\'t be greater than 255')
    return errors


def validate_range_checkbox(range_min, range_max):
    """
    Validates checkbox range (from 0)
    :param range_min:
    :param range_max:
    :return:
    """
    errors = []
    if range_min and range_min < 0:
        errors.append('Min range must\'t be less than 0')
    if range_max and range_max < 0:
        errors.append('Max range must\'t be less than 0')
    return errors
