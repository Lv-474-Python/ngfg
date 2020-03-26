"""
Test SheetManager
"""

import mock
import pytest
import googleapiclient

from app.helper.sheet_manager import SheetManager
from .helper_test_data import (
    SHEET_MANAGER_TEST_GET_DATA_WITH_RANGE_TRUE_DATA,
    SHEET_MANAGER_TEST_GET_DATA_WITH_RANGE_ERROR_DATA,
    SHEET_MANAGER_TEST_GET_ALL_DATA_ERROR_DATA,
    SHEET_MANAGER_TEST_GET_ALL_DATA_TRUE_DATA,
    SHEET_MANAGER_TEST_GET_ALL_DATA_ERROR_DATA,
    SHEET_MANAGER_TEST_APPEND_DATA_TRUE_DATA,
    SHEET_MANAGER_TEST_APPEND_DATA_VALUES_NOT_LIST_DATA,
    SHEET_MANAGER_TEST_APPEND_DATA_ERROR_DATA,
    SHEET_MANAGER_TEST_GET_SHEET_ID_FROM_URL_DATA,
    SHEET_MANAGER_TEST_LISTS_TO_LIST_DATA,
)


@pytest.mark.parametrize(
    "test_input, expected", 
    SHEET_MANAGER_TEST_GET_DATA_WITH_RANGE_TRUE_DATA
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


@pytest.mark.parametrize(
    "test_input, expected", 
    SHEET_MANAGER_TEST_GET_DATA_WITH_RANGE_ERROR_DATA
)
def test_get_data_with_range_error(test_input, expected):
    """
    Test SheetManager get_data_with_range()
    Test case when method raised googleapiclient.errors.HttpError

    :param test_input: test input data (spreadsheet_id, from_row, to_row)
    :param expected: test expected result
    """
    mock_patch_path = 'app.helper.sheet_manager.SheetManager.service.spreadsheets'
    with mock.patch(mock_patch_path) as mock_spreadsheets:
        mock_spreadsheets().values().get().execute.side_effect = googleapiclient.errors.HttpError('Test', b'Test')

        spreadsheet_id, from_row, to_row = test_input
        assert SheetManager.get_data_with_range(spreadsheet_id, from_row, to_row) == expected


@pytest.mark.parametrize(
    "spreadsheet_id, expected",
    SHEET_MANAGER_TEST_GET_ALL_DATA_TRUE_DATA
)
def test_get_all_data_true(spreadsheet_id, expected):
    """
    Test SheetManager get_all_data()
    Test case when method executed successfully

    :param spreadsheet_id: id of spreadsheet from which data will be retrieved
    :param expected: test expected result
    """
    mock_patch_path = 'app.helper.sheet_manager.SheetManager.service.spreadsheets'
    with mock.patch(mock_patch_path) as mock_spreadsheets:
        mock_spreadsheets().values().get().execute.return_value = {'values': [expected]}

        assert SheetManager.get_all_data(spreadsheet_id) == expected


@pytest.mark.parametrize(
    "spreadsheet_id, expected",
    SHEET_MANAGER_TEST_GET_ALL_DATA_ERROR_DATA
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


@pytest.mark.parametrize(
    "test_input, expected",
    SHEET_MANAGER_TEST_APPEND_DATA_TRUE_DATA
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


@pytest.mark.parametrize(
    "test_input, expected", 
    SHEET_MANAGER_TEST_APPEND_DATA_VALUES_NOT_LIST_DATA
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

@pytest.mark.parametrize(
    "test_input, expected",
    SHEET_MANAGER_TEST_APPEND_DATA_ERROR_DATA
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


@pytest.mark.parametrize(
    "url, expected",
    SHEET_MANAGER_TEST_GET_SHEET_ID_FROM_URL_DATA
)
def test_get_sheet_id_from_url(url, expected):
    """
    Test SheetManager get_sheet_id_from_url()

    :param url: url from which will be parsed sheet_id
    :param expected: test expected result
    """
    assert SheetManager.get_sheet_id_from_url(url) == expected

@pytest.mark.parametrize(
    "data, expected", 
    SHEET_MANAGER_TEST_LISTS_TO_LIST_DATA, 
    ids=["1_2_3_5", "1_2_2", "1_2_3_4", "None"]
)
def test_lists_to_list(data, expected):
    """
    Test SheetManager get_sheet_id_from_url()

    :param data: user data
    :param expected: test expected result
    """
    assert SheetManager.lists_to_list(data) == expected
