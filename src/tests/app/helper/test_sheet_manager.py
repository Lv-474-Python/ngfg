


"""
Test UserService
"""

# import mock
import pytest
from pytest_mock import mocker

# from tests import SheetManager
from app.helper.sheet_manager import SheetManager


@pytest.fixture
def sheet_manager():
    return SheetManager()


TEST_LISTS_TO_LIST_DATA = [
    ([[1, 2], [3, 5]], [1, 2, 3, 5]),
    ([[[1, 2], [2]]], [1, 2, 2]),
    ([1, 2, 3, 4], [1, 2, 3, 4]),
    (None, None)
]

@pytest.mark.parametrize(
    "test_input, expected", 
    TEST_LISTS_TO_LIST_DATA, 
    ids=["1_2_3_5", "1_2_2", "1_2_3_4", "None"]
)
def test_lists_to_list(sheet_manager, test_input, expected):
    assert sheet_manager.lists_to_list(test_input) == expected


TEST_GET_SHEET_ID_FROM_URL_DATA = [
    ("https://docs.google.com/spreadsheets/d/1fKRIFn2gs", "1fKRIFn2gs"),
    ("https://docs.google.com/spreadsheets/d/sad21d", "sad21d"),
    ("https://docs.google.com/spreadsheets/d/u_RIF", "u_RIF"),
    ("https://docs.google.com/spreadsheets/d/fuasdpa", "fuasdpa")
]

@pytest.mark.parametrize(
    "test_input, expected",
    TEST_GET_SHEET_ID_FROM_URL_DATA,
)
def test_get_sheet_id_from_url(sheet_manager, test_input, expected):
    assert sheet_manager.get_sheet_id_from_url(test_input) == expected


TEST_GET_DATA_WITH_RANGE = [
    (("1VgEe6d91mWE9VF54xkeJK6pKVKl_TjlsFPSGt3UtUx0", 'A1', 'A13'), ['Rivne', 'Lviv', 'London', 'Kyiv', 'Lutsk', 'Tokyo', 'Delhi', 'Paris', 'Chicago', 'Boston', 'Toronto', 'Madrid', 'Rome']),
]

@pytest.mark.parametrize(
    "test_input, expected",
    TEST_GET_DATA_WITH_RANGE,
)
def test_get_data_with_range(sheet_manager, test_input, expected):
    # mocker.patch('SheetManager.service.spreadsheets().values().get().execute')
    spreadsheet_id, from_row, to_row = test_input
    assert sheet_manager.get_data_with_range(spreadsheet_id, from_row, to_row) == expected
