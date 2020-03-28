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
    } ),
]

FIELD_SERVICE_GET_ADDITIONAL_OPTIONS_ERROR_DATA = [
    (9, 4),
    (10, 6),
]

FIELD_SERVICE_CHECK_FOR_RANGE_DATA = [
    ({'range': {'min': 2, 'max': 4}}, (2, 4)),
    ({}, (None, None))
]
