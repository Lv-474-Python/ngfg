"""
Choice options validator
"""


def check_for_repeated_options(options):
    """
    Checks if are repeated options in incoming parameter options
    :param options:
    :return:
    """
    if options is not None:
        if len(options) != len(set(options)):
            return True
    return False


def check_for_same_options(added, removed):
    """
    Checks if are same values in two lists
    :param added:
    :param removed:
    :return:
    """
    if added and removed:
        return bool(set(added) & set(removed))
    return False


def validate_repeats_of_choice_options(added, removed):
    """
    Validates if same values are repeated in added or removed or are in two lists
    :param added:
    :param removed:
    :return:
    """
    errors = []
    if check_for_repeated_options(options=added):
        errors.append('Repeated added values')
    if check_for_repeated_options(options=removed):
        errors.append('Repeated removed values')
    if check_for_same_options(added=added, removed=removed):
        errors.append('Identical values in added and removed options')
    return errors
