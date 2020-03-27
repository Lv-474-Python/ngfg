"""
Services test data
"""

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
