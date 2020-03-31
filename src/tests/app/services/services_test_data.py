"""
Services test data
"""

# FieldService
FIELD_SERVICE_CREATE_TEXT_OR_NUMBER_FIELD_WITHOUT_RANGE_DATA = [
    ("age", 1, 1, False),
    ("towns", 2, 1, True)
]

FIELD_SERVICE_CREATE_TEXT_OR_NUMBER_FIELD_WITH_RANGE_DATA = [
    ("name", 3, 1, False, 2, None),
    ("city", 4, 2, True, 2, 5)
]

FIELD_SERVICE_CREATE_TEXT_OR_NUMBER_FIELD_ERROR_DATA = [
    ("school", 5, 2),
    ("university", 6, 2)
]

FIELD_SERVICE_CREATE_TEXT_AREA_TRUE_DATA = [
    ("age", 7, 3),
    ("towns", 8, 3)
]

FIELD_SERVICE_CREATE_TEXT_AREA_ERROR_DATA = [
    ("first school", 9, 3),
    ("first university", 10, 3)
]

FIELD_SERVICE_CREATE_RADIO_FIELD_TRUE_DATA = [
    ("age", 11, 4, ["10", "11", "12"], True),
    ("towns", 12, 4, ["Rivne", "Lviv"], False)
]

FIELD_SERVICE_CREATE_RADIO_FIELD_NOT_OPTIONS_DATA = [
    ("words", 13, 4, []),
    ("text", 14, 4, None)
]

FIELD_SERVICE_CREATE_RADIO_FIELD_NOT_FIELD_DATA = [
    ("colors", 15, 4, ["r", "g", "b"]),
    ("cmyk", 16, 4, ["c", "m", "y", "k"])
]

FIELD_SERVICE_CREATE_CHECKBOX_FIELD_WITHOUT_RANGE_DATA = [
    ("age", 17, 6, ["10", "11", "12"], True),
    ("cities", 18, 6, ["Kyiv", "Lviv"], False)
]

FIELD_SERVICE_CREATE_CHECKBOX_FIELD_WITH_RANGE_DATA = [
    ("age", 19, 6, ["10", "11", "12"], True, 1, 2),
    ("clowns", 20, 6, ["Kyiv", "Lviv"], False, 1, None)
]

FIELD_SERVICE_CREATE_CHECKBOX_FIELD_ERROR_DATA = [
    ("beasts", 21, 5, []),
    ("elks", 22, 5, [])
]

FIELD_SERVICE_CREATE_AUTOCOMPLETE_FIELD_TRUE_DATA = [
    ("age", 23, 5, "data_url 1", "sheet 1", "A1", "A11"),
    ("towns", 24, 5, "data_url 2", "sheet 2", "B12", "B15"),
]

FIELD_SERVICE_CREATE_AUTOCOMPLETE_FIELD_NOT_FIELD_DATA = [
    ("crowns", 25, 5, "data_url 3", "sheet 3", "C1", "C11"),
    ("towns", 26, 5, "data_url 4", "sheet 4", "D12", "D15")
]

FIELD_SERVICE_CREATE_AUTOCOMPLETE_FIELD_NOT_SETTINGS_DATA = [
    ("clowns", 27, 5, "data_url 5", "sheet 5", "K1", "K11"),
    ("towns", 28, 5, "data_url 6", "sheet 6", "F12", "F15")
]

FIELD_SERVICE_GET_TEXT_OR_NUMBER_ADDITIONAL_OPTIONS_TRUE_DATA = [
    ("age", 29, 1, True, 1, 2),
    ("name", 30, 1, True, 1, None)
]

FIELD_SERVICE_GET_TEXT_OR_NUMBER_ADDITIONAL_OPTIONS_EMPTY_DATA = [
    (("surname", 31, 2), {}),
    (("last name", 32, 2), {})
]

FIELD_SERVICE_GET_CHOICE_ADDITIONAL_OPTIONS_TRUE_DATA = [
    (1, ["1", "2", "3"], 2, 3),
    (1, ["4", "4", "5"], 2, None)
]

FIELD_SERVICE_GET_CHOICE_ADDITIONAL_OPTIONS_ERROR_DATA = [1, 2]

FIELD_SERVICE_GET_AUTOCOMPLETE_ADDITIONAL_OPTIONS_TRUE_DATA = [
    (1, "http://docs.google.com/spreadsheet/d/asda", "sheet 1", "A1", "A2", ["1.1", "1.2"]),
    (2, "http://docs.google.com/spreadsheet/d/wsrs", "sheet 2", "B1", "B2", ["2.1", "2.2"])
]

FIELD_SERVICE_GET_AUTOCOMPLETE_ADDITIONAL_OPTIONS_ERROR_DATA = [1, 2]

FIELD_SERVICE_GET_ADDITIONAL_OPTIONS_NUMBER_TEXT_DATA = [
    (1, 1, {'isStrict': True, 'range': {'min': 5, 'max': 10}}),
    (1, 2, {'isStrict': False, 'range': {'min': 1, 'max': 10}}),
]

FIELD_SERVICE_GET_ADDITIONAL_OPTIONS_TEXT_AREA_DATA = [
    (4, 3, {}),
    (5, 3, {}),
]

FIELD_SERVICE_GET_ADDITIONAL_OPTIONS_RADIO_CHECKBOX_DATA = [
    (6, 4, {'choiceOptions': ['Yes', 'No']}),
    (7, 6, {'choiceOptions': ['Male', 'Female', 'Other'], 'range': {'min': 1, 'max': 2}}),
]

FIELD_SERVICE_GET_ADDITIONAL_OPTIONS_AUTOCOMPLETE_DATA = [
    (8, 5, {
        'settingAutocomplete': {
            'dataUrl': 'http://docs.google.com/spreadsheet/d/a',
            'sheet': 'sheet',
            'fromRow': 'A1',
            'toRow': 'A2'
        },
        'values': ['male', 'female']
    }),
    (9, 5, {
        'settingAutocomplete': {
            'dataUrl': 'http://docs.google.com/spreadsheet/d/aasd',
            'sheet': 'sheet 2',
            'fromRow': 'B1',
            'toRow': 'C2'
        },
        'values': ['yes', 'no']
    }),
]

FIELD_SERVICE_GET_ADDITIONAL_OPTIONS_ERROR_DATA = [
    (9, 4),
    (10, 6),
]

FIELD_SERVICE_CHECK_FOR_RANGE_DATA = [
    ({'range': {'min': 2, 'max': 4}}, (2, 4)),
    ({}, (None, None))
]

FIELD_SERVICE_VALIDATE_POST_FIELD_EXISTING = [
    (({'name': 'first_name', 'owner_id': 1, 'field_type': 1, 'is_strict': True},
     {'name': 'first_name', 'fieldType': 1}),
     (False, {'is_exist': 'Field with such name already exist'})),
    (({'name': 'cities', 'owner_id': 1, 'field_type': 4, 'is_strict': False},
     {'name': 'cities', 'fieldType': 4, 'choiceOptions': ['Lviv', 'Kyiv']}),
     (False, {'is_exist': 'Field with such name already exist'}))
]

FIELD_SERVICE_VALIDATE_POST_FIELD = [
    (({'name': 'city'}, 1), (False, {'fieldType': ['Missing data for required field.']})),
    (({'fieldType': 1}, 1), (False, {'name': ['Missing data for required field.']})),
    (({'name': 'city', 'fieldType': 4, 'choiceOptions': ['Lviv', 'Kyiv']}, 1), (True, {})),
    (({'name': 'first_name', 'fieldType': 1, 'isStrict': True}, 1), (True, {}))
]


FIELD_SERVICE_VALIDATE_POST_SETTING_AUTOCOMPLETE = [
    ({
        'name': 'cities',
        'fieldType': 5,
        'settingAutocomplete': {
            'dataUrl': "http://docs.google.com/spreadsheet/d/abcd",
            'sheet': 'sheet',
            'fromRow': 'A1',
            'toRow': 'A2'
        }
    }, (True, {})),

    ({'name': 'cities', 'fieldType': 5}, (False, {'settingAutocomplete': ['Missing data for required field.']})),

    ({
        'name': 'cities',
        'fieldType': 5,
        'unknownField': 'unknown value',
        'settingAutocomplete': {
            'dataUrl': "http://docs.google.com/spreadsheet/d/abcd",
            'sheet': 'sheet',
            'fromRow': 'A1',
            'toRow': 'A2'
        }
    }, (False, {'unknownField': ['Unknown field.']}))
]

FIELD_SERVICE_VALIDATE_POST_TEXT_OR_NUMBER = [
    ({
        'name': 'firstname',
        'fieldType': 1,
        'range': {
            'min': 1,
            'max': 15
        }
    }, (True, {})),
    ({'name': 'age', 'fieldType': 2, 'isStrict': True}, (True, {})),
    ({'name': 'age'}, (False, {'fieldType': ['Missing data for required field.']})),
    ({
        'name': 'age',
        'fieldType': 2,
        'unknownField': 'unknown value',
        'range': {
            'min': 13,
            'max': 99
        }
    }, (False, {'unknownField': ['Unknown field.']}))
]

FIELD_SERVICE_VALIDATE_POST_RADIO = [
    ({'name': 'gender', 'fieldType': 4, 'choiceOptions': ['Male', 'Female']}, (True, {})),
    ({'name': 'gender', 'fieldType': 4}, (False, {'choiceOptions': ['Missing data for required field.']})),
    ({
         'name': 'gender',
         'fieldType': 4,
         'choice_options': ['Male', 'Female'],
         'choiceOptions':['Male', 'Female']
     }, (False, {'choice_options': ['Unknown field.']}))
]

FIELD_SERVICE_VALIDATE_POST_CHECKBOX = [
    ({
        "name": "hobbies",
        "fieldType": 6,
        "range": {
            "min": 1,
            "max": 3
        },
        "choiceOptions": [
            "Writing", "Painting", "Coding"
        ]
    }, (True, {})),
    ({
        "name": "hobbies",
        "fieldType": 6,
        "range": {
            "min": 1,
            "max": 3
        }
    }, (False, {"choiceOptions": ["Missing data for required field."]})),
    ({
        "name": "hobbies",
        "fieldType": 6,
        "isStrict": True,
        "choiceOptions": [
            "Writing", "Painting"
        ]
    }, (False, {"isStrict": ["Unknown field."]})),
    ({
        "name": "hobbies",
        "fieldType": 6,
        "range": {
            "min": 1,
            "max": 3
        },
        "choiceOptions": [
            "Writing", "Painting"
        ]
    }, (False, {"range": {"_schema": ["Max selective options must be less than list of options"]}}))
]

FIELD_SERVICE_VALIDATE_TEXTAREA_POST = [
    ({"name": "about", "fieldType": 3}, (True, {})),
    ({"name": "about", "fieldType": 3, "isStrict": True}, (False, {"isStrict": ["Unknown field."]})),
    ({"fieldType": 3}, (False, {"name": ["Missing data for required field."]}))
]

FIELD_SERVICE_VALIDATE_OPTIONS_UPDATE = [
    ((1, ["a", "b", "c"], [], {"choiceOptions": ["a", "d", "e"]}), ['Added choices already exist']),
    ((1, ["e", "f"], ["d"], {"choiceOptions": ["a", "b", "c"]}), ['Removed options don\'t exist']),
    ((1, [], ["a", "b", "c"], {"choiceOptions": ["a", "b", "c"]}), ["Can\'t delete all options"]),
    ((1, ["d","e"], ["b"], {"choiceOptions": ["a", "b", "c"]}), [])
]

FIELD_SERVICE_VALIDATE_RADIO_UPDATE = [
    ((1, {"addedChoiceOptions": ["a", "b", "c"]}, ["Added choices already exist"]),
     (False, {"choiceOptions": {"_schema": ["Added choices already exist"]}})),
    ((1, {"removedChoiceOptions": ["b"]}, ["Removed options don\'t exist"]),
     (False, {"choiceOptions": {"_schema": ["Removed options don\'t exist"]}})),
    ((1, {"removedChoiceOptions": ["a", "b", "c"]}, ["Can\'t delete all options"]),
     (False, {"choiceOptions": {"_schema": ["Can\'t delete all options"]}})),
    ((1, {"addedChoiceOptions": ["a"]}, []),
     (True, {}))
]

FIELD_SERVICE_VALIDATE_CHECKBOX_OPTIONS_AND_RANGE_UPDATE = [
    ((1, ["a", "b"], ["c"], {
        "choiceOptions": ["d", "e"],
        "range": {
            "min": 1,
            "max": 3
        }
    }, None, True), False),
    ((1, [], [], {
        "choiceOptions": ["a", "b", "c"]
    }, None, True), "Can\'t delete range that doesn\'t exist"),
    ((1, ["a"], [], {
        "choiceOptions": ["b", "c", "d"],
        "range": {
            "min": 5,
            "max": 4
        }
    }, None, None), "Current min choice range is greater than updated choice amount"),
    ((1, ["a"], ["b", "c"], {
        "choiceOptions": ["b", "c", "d", "e"],
        "range": {
            "min": 1,
            "max": 4
        }
    }, None, None), "Current max choice range is greater than updated choice amount"),
    ((1, [], [], {"choiceOptions": ["a", "b", "c"]}, {"min": 4, "max": 3}, None),
     "New min choice range is greater than updated choice amount"),
    ((1, [], [], {"choiceOptions": ["a", "b", "c"]}, {"min": 1, "max": 5}, None),
     "New max choice range is greater than updated choice amount")
]

FIELD_SERVICE_VALIDATE_CHECKBOX_UPDATE = [
    ((1, {
        "addedChoiceOptions": ["a", "b", "c"],
        "removedChoiceOptions": ["d"],
    }, ["Added choices already exist"], []),
     (False, {"choiceOptions": {"_schema": ["Added choices already exist"]}})),
    ((1, {
        "addedChoiceOptions": ["a", "b", "c"],
        "range": {
            "min": 1,
            "max": 10
        },
    }, [], ["New max choice range is greater than updated choice amount"]),
     (False, {"options_and_range_error": ["New max choice range is greater than updated choice amount"]})),
    ((1, {
        "addedChoiceOptions": ["a"],
        "range": {
            "min": 1,
            "max": 3
        }
    }, [], []),
    (True, {}))
]

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

# UserService
USER_SERVICE_CREATE_WITHOUT_FILTER_DATA = [
    ("kaic", "kaic@gmail.com", "asdsadaa"),
    ("lsoa", "lsoa@gmail.com", "2fas2af")
]

USER_SERVICE_CREATE_WITH_FILTER_DATA = [
    ("kaic", "kaic@gmail.com", "asdsadaa"),
    ("lsoa", "lsoa@gmail.com", "2fas2af")
]

USER_SERVICE_GET_BY_ID_DATA = [
    (1, "kaidac", "kwqaic@gmail.com", "asdsadaa"),
    (2, "lsodsaa", "lssadoa@gmail.com", "2fas2af")
]

USER_SERVICE_UPDATE_DATA = [
    (1, None, None, None, None),
    (2, "lsodsaa", None, None, None),
    (3, "laaasqwq", "la3a@gmai.com", None, None),
    (4, "sqqasqwq", "laa@gmai.com", "asda", None),
    (5, "laaajnvvmm", "pos42a@gmai.com", "oda1", True),
    (6, "laaajndsam", "po1c2a@gmai.com", "ytrp", False)
]

USER_SERVICE_UPDATE_ERROR_DATA = [1, 2]

USER_SERVICE_DELETE_DATA = [1, 2]

USER_SERVICE_DELETE_ERROR_DATA = [1, 2]

USER_SERVICE_FILTER_BY_USERNAME_DATA = ["sda", "lsodsaa"]

USER_SERVICE_FILTER_BY_EMAIL_DATA = ["sda@gmail.com", "lsodsaa@gmail.com"]

USER_SERVICE_FILTER_BY_GOOGLE_TOKEN_DATA = ["sda@gmail.com", "lsodsaa@gmail.com"]

USER_SERVICE_FILTER_BY_IS_ACTIVE_DATA = [True, False]

USER_SERVICE_FILTER_BY_ALL_DATA = [
    ("aasdasda", "ada@gmail.com", "asdsada", True),
    ("gd2as", "adacv@gmail.com", "2asd2", False)
]

USER_SERVICE_CREATE_USER_BY_EMAIL_DATA = ["ladi@gmail.com"]
