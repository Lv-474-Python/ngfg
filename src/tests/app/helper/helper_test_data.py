"""
Helper test data
"""

# sheet_manager.py
SHEET_MANAGER_TEST_GET_DATA_WITH_RANGE_TRUE_DATA = [
    (("1Vg2q1qeksamWE9", 'A1', 'A13'), ['test1.1', 'test1.2']),
    (("1Vg1yuasdasddsa", 'A100', 'A130'), ['test2.1', 'test2.2']),
]

SHEET_MANAGER_TEST_GET_DATA_WITH_RANGE_ERROR_DATA = [
    (("1VgEe6d91mWE9VF54xkeJK6p", 'A1', 'A13'), None)
]

SHEET_MANAGER_TEST_GET_ALL_DATA_ERROR_DATA = [
    (("aWva1frw3lsdap"), None)
]

SHEET_MANAGER_TEST_GET_ALL_DATA_TRUE_DATA = [
    (("aWva1frw3lp"), ['test1.1', 'test1.2']),
    (("1Vg1yuasda2"), ['test2.1', 'test2.2']),
]

SHEET_MANAGER_TEST_GET_ALL_DATA_ERROR_DATA = [
    (("aWva1frw3lsdap"), None)
]

SHEET_MANAGER_TEST_APPEND_DATA_TRUE_DATA = [
    (("aWva1frw3lp", [10, 20]), True),
    (("1Vg1yuasda2", ['test1.1', 'test1.2', ['radio 1', 'radio 2']]), True),
]

SHEET_MANAGER_TEST_APPEND_DATA_VALUES_NOT_LIST_DATA = [
    (("aWva1frw3lp", 10), None),
    (("aWva1frw3lp", 'test data'), None)
]

SHEET_MANAGER_TEST_APPEND_DATA_ERROR_DATA = [
    (("aWva1frw3lp", [1, 2, 3]), None),
    (("1Vg1yuasda2", ['test1', 'test1.']), None),
]

SHEET_MANAGER_TEST_GET_SHEET_ID_FROM_URL_DATA = [
    ("https://docs.google.com/spreadsheets/d/1fKRIFn2gs", "1fKRIFn2gs"),
    ("https://docs.google.com/spreadsheets/d/sad21d", "sad21d"),
    ("https://docs.google.com/spreadsheets/d/u_RIF", "u_RIF")
]

SHEET_MANAGER_TEST_LISTS_TO_LIST_DATA = [
    ([[1, 2], [3, 5]], [1, 2, 3, 5]),
    ([[[1, 2], [2]]], [1, 2, 2]),
    ([1, 2, 3, 4], [1, 2, 3, 4]),
    (None, None)
]
