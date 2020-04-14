"""
Routers test data
"""

# field.py
FIELD_RESOURCE_GET_ALL_TRUE_WITH_EXTRA_OPTIONS = [
    (
        {'id': 1, 'name': 'name 1', 'owner_id': 1, 'field_type': 1, 'is_strict': True},
        {'range': {'min': 10, 'max': 100}},
        {'id': 2, 'username': 'name 1', 'email': 'ma@gmail.com', 'google_token': 'aq'}
    ),
    (
        {'id': 2, 'name': 'name 2', 'owner_id': 2, 'field_type': 2, 'is_strict': True},
        {'range': {'min': 100, 'max': 150}},
        {'id': 3, 'username': 'name 3', 'email': 'm2@gmail.com', 'google_token': 'wq'}
    ),
    (
        {'id': 3, 'name': 'name 3', 'owner_id': 3, 'field_type': 3},
        {},
        {'id': 4, 'username': 'name 4', 'email': 'm4@gmail.com', 'google_token': 'af'}
    ),
    (
        {'id': 4, 'name': 'name 4', 'owner_id': 4, 'field_type': 4},
        {'choiceOptions': ['1', '2', '3', '4', '5']},
        {'id': 5, 'username': 'name 5', 'email': 'mp@gmail.com', 'google_token': 'rq'}
    ),
    (
        {'id': 5, 'name': 'name 5', 'owner_id': 5, 'field_type': 5},
        {
            'settingAutocomplete': {
                'dataUrl': 'https://docs.google.com/spreadsheet/d/aua',
                'sheet': 'sheet1',
                'fromRow': 'A1',
                'toRow': 'A13'
            },
            'values': ['1', '2', '3', '4']
        },
        {'id': 6, 'username': 'name 6', 'email': 'md@gmail.com', 'google_token': 'ew'}
    ),
    (
        {'id': 6, 'name': 'name 6', 'owner_id': 6, 'field_type': 6},
        {'choiceOptions': ['1', '2', '3', '4'], 'range': {'min': 1, 'max': 2}},
        {'id': 7, 'username': 'name 9', 'email': 'ms@gmail.com', 'google_token': 'al'}
    )
]

FIELD_RESOURCE_GET_ALL_TRUE_WITHOUT_EXTRA_OPTIONS = [
    (
        {'id': 1, 'name': 'name 1', 'owner_id': 1, 'field_type': 1, 'is_strict': True},
        {'id': 2, 'username': 'name 1', 'email': 'ma@gmail.com', 'google_token': 'aq'}
    ),
    (
        {'id': 2, 'name': 'name 2', 'owner_id': 2, 'field_type': 2, 'is_strict': True},
        {'id': 3, 'username': 'name 3', 'email': 'm2@gmail.com', 'google_token': 'wq'}
    ),
    (
        {'id': 3, 'name': 'name 3', 'owner_id': 3, 'field_type': 3},
        {'id': 4, 'username': 'name 4', 'email': 'm4@gmail.com', 'google_token': 'af'}
    ),
    (
        {'id': 4, 'name': 'name 4', 'owner_id': 4, 'field_type': 4},
        {'id': 5, 'username': 'name 5', 'email': 'mp@gmail.com', 'google_token': 'rq'}
    ),
    (
        {'id': 5, 'name': 'name 5', 'owner_id': 5, 'field_type': 5},
        {'id': 6, 'username': 'name 6', 'email': 'md@gmail.com', 'google_token': 'ew'}
    ),
    (
        {'id': 6, 'name': 'name 6', 'owner_id': 6, 'field_type': 6},
        {'id': 7, 'username': 'name 9', 'email': 'ms@gmail.com', 'google_token': 'al'}
    )
]

FIELD_RESOURCE_GET_ALL_TRUE_WITH_SHARED_FIELDS = [
    (
        {'id': 1, 'name': 'name 1', 'owner_id': 1, 'field_type': 1, 'is_strict': True},
        {'id': 2, 'username': 'name 1', 'email': 'ma@gmail.com', 'google_token': 'aq'}
    ),
    (
        {'id': 2, 'name': 'name 2', 'owner_id': 2, 'field_type': 2, 'is_strict': True},
        {'id': 3, 'username': 'name 3', 'email': 'm2@gmail.com', 'google_token': 'wq'}
    ),
    (
        {'id': 3, 'name': 'name 3', 'owner_id': 3, 'field_type': 3},
        {'id': 4, 'username': 'name 4', 'email': 'm4@gmail.com', 'google_token': 'af'}
    ),
    (
        {'id': 4, 'name': 'name 4', 'owner_id': 4, 'field_type': 4},
        {'id': 5, 'username': 'name 5', 'email': 'mp@gmail.com', 'google_token': 'rq'}
    ),
    (
        {'id': 5, 'name': 'name 5', 'owner_id': 5, 'field_type': 5},
        {'id': 6, 'username': 'name 6', 'email': 'md@gmail.com', 'google_token': 'ew'}
    ),
    (
        {'id': 6, 'name': 'name 6', 'owner_id': 6, 'field_type': 6},
        {'id': 7, 'username': 'name 9', 'email': 'ms@gmail.com', 'google_token': 'al'}
    )
]

FIELD_RESOURCE_GET_BY_ID_TRUE_WITH_EXTRA_OPTIONS = [
    (
        {'id': 1, 'name': 'name 1', 'owner_id': 1, 'field_type': 1, 'is_strict': True},
        {'range': {'min': 10, 'max': 100}}
    ),
    (
        {'id': 2, 'name': 'name 2', 'owner_id': 1, 'field_type': 2, 'is_strict': True},
        {'range': {'min': 100, 'max': 150}}
    ),
    (
        {'id': 3, 'name': 'name 3', 'owner_id': 1, 'field_type': 3},
        {}
    ),
    (
        {'id': 4, 'name': 'name 4', 'owner_id': 1, 'field_type': 4},
        {'choiceOptions': ['1', '2', '3', '4', '5']}
    ),
    (
        {'id': 5, 'name': 'name 5', 'owner_id': 1, 'field_type': 5},
        {
            'settingAutocomplete': {
                'dataUrl': 'https://docs.google.com/spreadsheet/d/aua',
                'sheet': 'sheet1',
                'fromRow': 'A1',
                'toRow': 'A13'
            },
            'values': ['1', '2', '3', '4']
        }
    ),
    (
        {'id': 6, 'name': 'name 6', 'owner_id': 1, 'field_type': 6},
        {'choiceOptions': ['1', '2', '3', '4'], 'range': {'min': 1, 'max': 2}}
    )
]

FIELD_RESOURCE_GET_BY_ID_TRUE_WITHOUT_EXTRA_OPTIONS = [
    {'id': 1, 'name': 'name 1', 'owner_id': 1, 'field_type': 1, 'is_strict': True},
    {'id': 2, 'name': 'name 2', 'owner_id': 1, 'field_type': 2, 'is_strict': True},
    {'id': 3, 'name': 'name 3', 'owner_id': 1, 'field_type': 3},
    {'id': 4, 'name': 'name 4', 'owner_id': 1, 'field_type': 4},
    {'id': 5, 'name': 'name 5', 'owner_id': 1, 'field_type': 5},
    {'id': 6, 'name': 'name 6', 'owner_id': 1, 'field_type': 6}
]

FIELD_RESOURCE_GET_BY_ID_FORBIDDEN = [
    ({'id': 2, 'name': 'name 1', 'owner_id': 2, 'field_type': 1}),
    ({'id': 3, 'name': 'name 1', 'owner_id': 3, 'field_type': 1}),
    ({'id': 4, 'name': 'name 1', 'owner_id': 4, 'field_type': 1}),
]
