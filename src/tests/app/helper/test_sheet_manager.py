"""
Test SheetManager
"""

import mock
import pytest
import googleapiclient

from app.helper.sheet_manager import SheetManager


TEST_GET_DATA_WITH_RANGE_TRUE_DATA = [
    (("1Vg2q1qeksamWE9", 'A1', 'A13'), ['test1.1', 'test1.2']),
    (("1Vg1yuasdasddsa", 'A100', 'A130'), ['test2.1', 'test2.2']),
]
@pytest.mark.parametrize(
    "test_input, expected", 
    TEST_GET_DATA_WITH_RANGE_TRUE_DATA
)
def test_get_data_with_range_true(test_input, expected):
    """
    Test SheetManager get_data_with_range()
    Test case when method executed successfully

    :param test_input: test input data (spreadsheet_id, from_row, to_row)
    :param expected: test expected result
    """
    mock_patch_path = 'app.helper.sheet_manager.SheetManager.service.spreadsheets'
    with mock.patch(mock_patch_path) as mock_execute:
        mock_execute().values().get().execute.return_value = {'values': [expected]}

        spreadsheet_id, from_row, to_row = test_input
        assert SheetManager.get_data_with_range(spreadsheet_id, from_row, to_row) == expected


TEST_GET_DATA_WITH_RANGE_ERROR_DATA = [
    (("1VgEe6d91mWE9VF54xkeJK6p", 'A1', 'A13'), None)
]
@pytest.mark.parametrize(
    "test_input, expected", 
    TEST_GET_DATA_WITH_RANGE_ERROR_DATA
)
def test_get_data_with_range_error(test_input, expected):
    """
    Test SheetManager get_data_with_range()
    Test case when method raised googleapiclient.errors.HttpError

    :param test_input: test input data (spreadsheet_id, from_row, to_row)
    :param expected: test expected result
    """
    mock_patch_path = 'app.helper.sheet_manager.SheetManager.service.spreadsheets'
    with mock.patch(mock_patch_path) as mock_execute:
        mock_execute().values().get().execute.side_effect = googleapiclient.errors.HttpError('Test', b'Test')

        spreadsheet_id, from_row, to_row = test_input
        assert SheetManager.get_data_with_range(spreadsheet_id, from_row, to_row) == expected


TEST_GET_ALL_DATA_TRUE_DATA = [
    (("aWva1frw3lp"), ['test1.1', 'test1.2']),
    (("1Vg1yuasda2"), ['test2.1', 'test2.2']),
]
@pytest.mark.parametrize(
    "spreadsheet_id, expected",
    TEST_GET_ALL_DATA_TRUE_DATA
)
def test_get_all_data_true(spreadsheet_id, expected):
    """
    Test SheetManager get_all_data()
    Test case when method executed successfully

    :param spreadsheet_id: id of spreadsheet from which data will be retrieved
    :param expected: test expected result
    """
    mock_patch_path = 'app.helper.sheet_manager.SheetManager.service.spreadsheets'
    with mock.patch(mock_patch_path) as mock_execute:
        mock_execute().values().get().execute.return_value = {'values': [expected]}

        assert SheetManager.get_all_data(spreadsheet_id) == expected


TEST_GET_ALL_DATA_ERROR_DATA = [
    (("aWva1frw3lsdap"), None)
]
@pytest.mark.parametrize(
    "spreadsheet_id, expected",
    TEST_GET_ALL_DATA_ERROR_DATA
)
def test_get_all_data_raised_error(spreadsheet_id, expected):
    """
    Test SheetManager get_all_data()
    Test case when method raised googleapiclient.errors.HttpError

    :param spreadsheet_id: id of spreadsheet from which data will be retrieved
    :param expected: test expected result
    """
    mock_patch_path = 'app.helper.sheet_manager.SheetManager.service.spreadsheets'
    with mock.patch(mock_patch_path) as mock_spreadsheets:
        mock_spreadsheets().values().get().execute.side_effect = googleapiclient.errors.HttpError('Test', b'Test')

        assert SheetManager.get_all_data(spreadsheet_id) == expected


TEST_APPEND_DATA_TRUE_DATA = [
    (("aWva1frw3lp", [10, 20]), True),
    (("1Vg1yuasda2", ['test1.1', 'test1.2', ['radio 1', 'radio 2']]), True),
]
@pytest.mark.parametrize(
    "test_input, expected", 
    TEST_APPEND_DATA_TRUE_DATA
)
def test_append_data_true(test_input, expected):
    """
    Test SheetManager append_data()
    Test case when method executed successfully

    :param test_input: test input data (spreadsheet_id, values)
    :param expected: test expected result
    """
    with mock.patch('app.helper.sheet_manager.SheetManager.service.spreadsheets') as mock_spreadsheets:
        mock_spreadsheets().values().append().execute.return_value = None

        spreadsheet_id, values = test_input
        assert SheetManager.append_data(spreadsheet_id, values) == expected


TEST_APPEND_DATA_VALUES_NOT_LIST_DATA = [
    (("aWva1frw3lp", 10), None),
    (("aWva1frw3lp", 'test data'), None)
]
@pytest.mark.parametrize(
    "test_input, expected", 
    TEST_APPEND_DATA_VALUES_NOT_LIST_DATA
)
def test_append_data_values_not_list(test_input, expected):
    """
    Test SheetManager append_data()
    Test case when variable values isn't list   ???

    :param test_input: test input data (spreadsheet_id, values)
    :param expected: test expected result
    """
    spreadsheet_id, values = test_input
    assert SheetManager.append_data(spreadsheet_id, values) == expected


TEST_APPEND_DATA_ERROR_DATA = [
    (("aWva1frw3lp", [1, 2, 3]), None),
    (("1Vg1yuasda2", ['test1', 'test1.']), None),
]
@pytest.mark.parametrize(
    "test_input, expected",
    TEST_APPEND_DATA_ERROR_DATA
)
def test_get_all_data_error(test_input, expected):
    """
    Test SheetManager get_all_data()
    Test case when method raised googleapiclient.errors.HttpError

    :param test_input: test input data (spreadsheet_id, values)
    :param expected: test expected result
    """
    mock_patch_path = 'app.helper.sheet_manager.SheetManager.service.spreadsheets'
    with mock.patch(mock_patch_path) as mock_spreadsheets:
        mock_spreadsheets().values().append().execute.side_effect = googleapiclient.errors.HttpError('Test', b'Test')

        spreadsheet_id, values = test_input
        assert SheetManager.append_data(spreadsheet_id, values) == expected



TEST_GET_SHEET_ID_FROM_URL_DATA = [
    ("https://docs.google.com/spreadsheets/d/1fKRIFn2gs", "1fKRIFn2gs"),
    ("https://docs.google.com/spreadsheets/d/sad21d", "sad21d"),
    ("https://docs.google.com/spreadsheets/d/u_RIF", "u_RIF")
]
@pytest.mark.parametrize(
    "url, expected",
    TEST_GET_SHEET_ID_FROM_URL_DATA,
)
def test_get_sheet_id_from_url(url, expected):
    """
    Test SheetManager get_sheet_id_from_url()

    :param url: url from which will be parsed sheet_id
    :param expected: test expected result
    """
    assert SheetManager.get_sheet_id_from_url(url) == expected



TEST_LISTS_TO_LIST_DATA = [
    ([[1, 2], [3, 5]], [1, 2, 3, 5]),
    ([[[1, 2], [2]]], [1, 2, 2]),
    ([1, 2, 3, 4], [1, 2, 3, 4]),
    (None, None)
]
@pytest.mark.parametrize(
    "data, expected", 
    TEST_LISTS_TO_LIST_DATA, 
    ids=["1_2_3_5", "1_2_2", "1_2_3_4", "None"]
)
def test_lists_to_list(data, expected):
    """
    Test SheetManager get_sheet_id_from_url()

    :param data: user data
    :param expected: test expected result
    """
    assert SheetManager.lists_to_list(data) == expected


# @mock.patch('app.helper.sheet_manager.SheetManager.a')
# def test_mock(mock_a):
#     mock_a.return_value = 10
#     assert SheetManager.a() == 10