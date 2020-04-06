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
    SHEET_MANAGER_TEST_GET_SHEET_ID_FROM_URL_ERROR_DATA,
    SHEET_MANAGER_TEST_LISTS_TO_LIST_DATA,
)


# get_data_with_range
@pytest.mark.parametrize(
    "test_input, expected",
    SHEET_MANAGER_TEST_GET_DATA_WITH_RANGE_TRUE_DATA
)
@mock.patch('app.helper.sheet_manager.SheetManager.service.spreadsheets')
def test_get_data_with_range_true(mock_spreadsheets, test_input, expected):
    """
    Test SheetManager get_data_with_range()
    Test case when method executed successfully
    """
    mock_spreadsheets().values().get().execute.return_value = {'values': [expected]}

    spreadsheet_id, from_row, to_row = test_input
    result = SheetManager.get_data_with_range(spreadsheet_id, from_row, to_row)

    assert result == expected


@pytest.mark.parametrize(
    "test_input, expected",
    SHEET_MANAGER_TEST_GET_DATA_WITH_RANGE_ERROR_DATA
)
@mock.patch('app.helper.sheet_manager.SheetManager.service.spreadsheets')
def test_get_data_with_range_error(mock_spreadsheets, test_input, expected):
    """
    Test SheetManager get_data_with_range()
    Test case when method raised googleapiclient.errors.HttpError
    """
    mock_spreadsheets().values().get().execute.side_effect = googleapiclient.errors.HttpError('Test', b'Test')

    spreadsheet_id, from_row, to_row = test_input
    result = SheetManager.get_data_with_range(spreadsheet_id, from_row, to_row)

    assert result == expected


# get_all_data
@pytest.mark.parametrize(
    "spreadsheet_id, expected",
    SHEET_MANAGER_TEST_GET_ALL_DATA_TRUE_DATA
)
@mock.patch('app.helper.sheet_manager.SheetManager.service.spreadsheets')
def test_get_all_data_true(mock_spreadsheets, spreadsheet_id, expected):
    """
    Test SheetManager get_all_data()
    Test case when method executed successfully
    """
    mock_spreadsheets().values().get().execute.return_value = {'values': [expected]}

    result = SheetManager.get_all_data(spreadsheet_id)

    assert result == expected


@pytest.mark.parametrize(
    "spreadsheet_id, expected",
    SHEET_MANAGER_TEST_GET_ALL_DATA_ERROR_DATA
)
@mock.patch('app.helper.sheet_manager.SheetManager.service.spreadsheets')
def test_get_all_data_raised_error(mock_spreadsheets, spreadsheet_id, expected):
    """
    Test SheetManager get_all_data()
    Test case when method raised googleapiclient.errors.HttpError
    """
    mock_spreadsheets().values().get().execute.side_effect = googleapiclient.errors.HttpError('Test', b'Test')

    result = SheetManager.get_all_data(spreadsheet_id)

    assert result == expected


# append_data
@pytest.mark.parametrize(
    "test_input, expected",
    SHEET_MANAGER_TEST_APPEND_DATA_TRUE_DATA
)
@mock.patch('app.helper.sheet_manager.SheetManager.service.spreadsheets')
def test_append_data_true(mock_spreadsheets, test_input, expected):
    """
    Test SheetManager append_data()
    Test case when method executed successfully
    """
    mock_spreadsheets().values().append().execute.return_value = None

    spreadsheet_id, values = test_input
    result = SheetManager.append_data(spreadsheet_id, values)

    assert result == expected


@pytest.mark.parametrize(
    "test_input, expected", 
    SHEET_MANAGER_TEST_APPEND_DATA_VALUES_NOT_LIST_DATA
)
def test_append_data_values_not_list(test_input, expected):
    """
    Test SheetManager append_data()
    Test case when variable values isn't list
    """
    spreadsheet_id, values = test_input
    result = SheetManager.append_data(spreadsheet_id, values)

    assert result == expected


@pytest.mark.parametrize(
    "test_input, expected",
    SHEET_MANAGER_TEST_APPEND_DATA_ERROR_DATA
)
@mock.patch('app.helper.sheet_manager.SheetManager.service.spreadsheets')
def test_append_data_error(mock_spreadsheets, test_input, expected):
    """
    Test SheetManager get_all_data()
    Test case when method raised googleapiclient.errors.HttpError
    """
    mock_spreadsheets().values().append().execute.side_effect = googleapiclient.errors.HttpError('Test', b'Test')

    spreadsheet_id, values = test_input
    result = SheetManager.append_data(spreadsheet_id, values)

    assert result == expected


# get_sheet_id_from_url
@pytest.mark.parametrize(
    "url, expected",
    SHEET_MANAGER_TEST_GET_SHEET_ID_FROM_URL_DATA
)
def test_get_sheet_id_from_url(url, expected):
    """
    Test SheetManager get_sheet_id_from_url()
    """
    result = SheetManager.get_sheet_id_from_url(url)

    assert result == expected


@pytest.mark.parametrize(
    "url",
    SHEET_MANAGER_TEST_GET_SHEET_ID_FROM_URL_ERROR_DATA
)
def test_get_sheet_id_from_url_error(url):
    """
    Test SheetManager get_sheet_id_from_url()
    Test case when method raised IndexError and returned None
    """
    result = SheetManager.get_sheet_id_from_url(url)

    assert result is None


# lists_to_list
@pytest.mark.parametrize(
    "data, expected",
    SHEET_MANAGER_TEST_LISTS_TO_LIST_DATA,
)
def test_lists_to_list(data, expected):
    """
    Test SheetManager lists_to_list()
    """
    result = SheetManager.lists_to_list(data)

    assert result == expected
