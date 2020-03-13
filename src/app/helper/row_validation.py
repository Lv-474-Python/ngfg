"""
Setting autocomplete rows validating methods
"""
import re


def validate_row(row):
    """
    Validates row
    :param row:
    :return:
    """
    splited_row = re.split('(\d+)', row)  # pylint:disable=anomalous-backslash-in-string
    if len(splited_row) > 3:
        return False
    if len(splited_row) > 1:
        if splited_row[2] != '':
            return False
    if len(splited_row[0]) > 3:
        return False
    return True
