"""
Test SheetManager
"""

import mock
import pytest
# from pytest_mock import mocker

# from tests import SheetManager
from app.helper.sheet_manager import SheetManager


TEST_LISTS_TO_LIST_DATA = [
    ([[1, 2], [3, 5]], [1, 2, 3, 5]),
    ([[[1, 2], [2]]], [1, 2, 2]),
    ([1, 2, 3, 4], [1, 2, 3, 4]),
    (None, None)
]

TEST_GET_SHEET_ID_FROM_URL_DATA = [
    ("https://docs.google.com/spreadsheets/d/1fKRIFn2gs", "1fKRIFn2gs"),
    ("https://docs.google.com/spreadsheets/d/sad21d", "sad21d"),
    ("https://docs.google.com/spreadsheets/d/u_RIF", "u_RIF"),
    ("https://docs.google.com/spreadsheets/d/fuasdpa", "fuasdpa")
]


TEST_GET_DATA_WITH_RANGE = [
    # (("1VgEe6d91mWE9VF54xkeJK6pKVKl_TjlsFPSGt3UtUx0", 'A1', 'A13'), ['Rivne', 'Lviv', 'London', 'Kyiv', 'Lutsk', 'Tokyo', 'Delhi', 'Paris', 'Chicago', 'Boston', 'Toronto', 'Madrid', 'Rome']),
    (("1VgEe6d91mWE9VF54xkeJK6pKVKl", 'A1', 'A13'), ['Rivne', 'Lviv']),
]


@pytest.mark.parametrize(
    "test_input, expected", 
    TEST_LISTS_TO_LIST_DATA, 
    ids=["1_2_3_5", "1_2_2", "1_2_3_4", "None"]
)
def test_lists_to_list(test_input, expected):
    assert SheetManager.lists_to_list(test_input) == expected

@pytest.mark.parametrize(
    "test_input, expected",
    TEST_GET_SHEET_ID_FROM_URL_DATA,
)
def test_get_sheet_id_from_url(test_input, expected):
    assert SheetManager.get_sheet_id_from_url(test_input) == expected


@pytest.mark.parametrize("test_input, expected", TEST_GET_DATA_WITH_RANGE)
# @mock.patch('app.helper.sheet_manager.SheetManager.service.spreadsheets.values.get.execute')
@mock.patch('app.helper.sheet_manager.SheetManager.service.spreadsheets')
def test_get_data_with_range(mock_execute, test_input, expected):
    # типу що я роблю - я мокаю до першого виклику (цей рядок) а далі руками дописую (і останній (функція остання) має бути без виклику, а просто (execute) як тут)
    mock_execute().values().get().execute.return_value = {'values': [expected]}
    # mock_execute.return_value = {'values': [expected]}

    # mock_execute.spreadsheets.return_value = \
    #     mock_execute.spreadsheets.values.return_value = \
    #         mock_execute.spreadsheets.values.get.return_value = \
    #             mock_execute.spreadsheets.values.get.execute.return_value = [expected]

    # import pdb; pdb.set_trace()

    # mock.patch('app.helper.sheet_manager.SheetManager.service.spreadsheets().values().get().execute', mock.MagicMock(return_value=['Rivne', 'Lviv']))

    spreadsheet_id, from_row, to_row = test_input
    assert SheetManager.get_data_with_range(spreadsheet_id, from_row, to_row) == expected


@mock.patch('app.helper.sheet_manager.SheetManager.a')
def test_mock(mock_a):
    mock_a.return_value = 10
    assert SheetManager.a() == 10
