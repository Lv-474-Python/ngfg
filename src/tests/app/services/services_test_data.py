"""
Services test data
"""


# FormService
FORM_SERVICE_CREATE_DATA = [
    (1, "login form", "login", "http://docs.google.com/spreadsheet/d/s1", True),
    (2, "feedback form", "feedback", "http://docs.google.com/spreadsheet/d/ad", False)
]

FORM_SERVICE_GET_BY_ID_DATA = [
    (1, 3, "login form", "login", "http://docs.google.com/spreadsheet/d/s1", True),
    (2, 4, "feedback form", "feedback", "http://docs.google.com/spreadsheet/d/ad", False)
]

FORM_SERVICE_UPDATE_DATA = [
    (1, None, None, None, None, None),
    (2, 5, None, None, None, None),
    (3, 6, "name 1", None, None, None),
    (4, 7, "name 2", "title 2", None, None),
    (5, 8, "name 3", "title 3", "http://docs.google.com/spreadsheet/d/s1", None),
    (6, 9, "name 4", "title 4", "http://docs.google.com/spreadsheet/d/s1", True),
    (7, 10, "name 5", "title 5", "http://docs.google.com/spreadsheet/d/s1", False)
]

FORM_SERVICE_UPDATE_ERROR_DATA = [1, 2]

FORM_SERVICE_DELETE_DATA = [1, 2]

FORM_SERVICE_DELETE_ERROR_DATA = [1, 2]

FORM_SERVICE_FILTER_BY_FORM_ID_DATA = [1, 2]

FORM_SERVICE_FILTER_BY_OWNER_ID_DATA = [3, 4]

FORM_SERVICE_FILTER_BY_NAME_DATA = ["form name 3", "form name 4"]

FORM_SERVICE_FILTER_BY_TITLE_DATA = ["form title 5", "form title 6"]

FORM_SERVICE_FILTER_BY_RESULT_URL_DATA = [
    "http://docs.google.com/spreadsheet/d/asda",
    "http://docs.google.com/spreadsheet/d/2sa1"
]

FORM_SERVICE_FILTER_BY_IS_PUBLISHED_DATA = [True, False]

FORM_SERVICE_FILTER_BY_ALL_DATA = [
    (1, 1, "name 7", "title 7", "http://docs.google.com/spreadsheet/d/asd", True),
    (2, 2, "name 8", "title 8", "http://docs.google.com/spreadsheet/d/g2a", False)
]
