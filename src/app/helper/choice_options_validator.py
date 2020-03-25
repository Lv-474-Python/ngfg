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
