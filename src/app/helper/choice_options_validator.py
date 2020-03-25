"""
Choice options validator
"""


def check_for_repeated_options(options):
    if options is not None:
        if len(options) != len(set(options)):
            return True
    return False


def check_for_same_options(added, removed):
    if added and removed:
        return bool(set(added) & set(removed))
    return False
