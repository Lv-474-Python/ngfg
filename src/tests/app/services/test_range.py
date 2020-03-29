"""
Tests for RangeService
"""

import pytest
import mock

from app.models import Range
from app.services import RangeService


@pytest.fixture()
def range_data():
    data = {
        "min": 0,
        "max": 1
    }
    return data


@pytest.fixture()
def range_data_with_id():
    data = {
        "id": 1,
        "min": 3,
        "max": 5
    }
    return data


@pytest.fixture()
def range_update_data():
    data = {
        'min': 0,
        'max': 1
    }
    return data


@mock.patch('app.models.Range.query')
def test_create_existing(mock_query, range_data):
    """
    Test RangeService create()
    Test case when Range.query returns existing value
    """
    range_instance = Range(min=range_data.get('min'), max=range_data.get('max'))
    mock_query.filter_by.return_value.first.return_value = range_instance

    test_instance = RangeService.create(range_min=range_data.get('min'), range_max=range_data.get('max'))

    assert test_instance.min == range_instance.min
    assert test_instance.max == range_instance.max


@mock.patch('app.DB.session.add')
@mock.patch('app.models.Range.query')
def test_create_not_existing(mock_query, mock_db_add, range_data):
    """
    Test RangeService create()
    Test case when Range.query returns None
    """
    range_instance = Range(min=range_data.get('min'), max=range_data.get('max'))
    mock_query.filter_by.return_value.first.return_value = None
    mock_db_add.return_value = None
    test_instance = RangeService.create(range_min=range_data.get('min'), range_max=range_data.get('max'))

    assert test_instance.min == range_instance.min
    assert test_instance.max == range_instance.max


@mock.patch('app.DB.session.merge')
@mock.patch('app.services.RangeService.get_by_id')
def test_update_min(mock_get_by_id, mock_db_merge, range_data_with_id, range_update_data):
    """
    Test RangeService update()
    Test case when only min value is updated
    """
    range_instance = Range(**range_data_with_id)
    updated_instance = Range(
        id=range_data_with_id.get('id'),
        min=range_update_data.get('min'),
        max=range_data_with_id.get('max')
    )
    mock_get_by_id.return_value = range_instance
    mock_db_merge.return_value = updated_instance
    test_update_result = RangeService.update(
        range_id=range_data_with_id.get('id'),
        range_min=range_update_data.get('min')
    )
    assert updated_instance.min == test_update_result.min


@mock.patch('app.DB.session.merge')
@mock.patch('app.services.RangeService.get_by_id')
def test_update_max(mock_get_by_id, mock_db_merge, range_data_with_id, range_update_data):
    """
    Test RangeService update()
    Test case when only max value is updated
    """
    range_instance = Range(**range_data_with_id)
    updated_instance = Range(
        id=range_data_with_id.get('id'),
        min=range_data_with_id.get('min'),
        max=range_update_data.get('max')
    )
    mock_get_by_id.return_value = range_instance
    mock_db_merge.return_value = updated_instance
    test_update_result = RangeService.update(
        range_id=range_data_with_id.get('id'),
        range_max=range_update_data.get('max')
    )
    assert updated_instance.max == test_update_result.max


@mock.patch('app.services.RangeService.get_by_id')
def test_update_nonexistent_range(mock_get_by_id, range_data_with_id):
    """
    Test RangeService update()
    Test case when get_by_id returns None
    """
    mock_get_by_id.return_value = None
    updated_instance = RangeService.update(range_id=range_data_with_id.get('id'))
    assert updated_instance is None


@mock.patch('app.DB.session.delete')
@mock.patch('app.services.RangeService.get_by_id')
def test_delete(mock_get_by_id, mock_db_delete, range_data_with_id):
    """
    Test RangeService delete()
    Test case when deletion is successful
    """
    mock_get_by_id.return_value = Range(**range_data_with_id)
    mock_db_delete.return_value = None
    test_delete_result = RangeService.delete(range_id=range_data_with_id.get('id'))
    assert test_delete_result is True


@mock.patch('app.services.RangeService.get_by_id')
def test_delete_nonexistent_range(mock_get_by_id, range_data_with_id):
    """
    Test RangeService delete()
    Test case when get_by_id returns None
    """
    mock_get_by_id.return_value = None
    test_delete_result = RangeService.delete(range_id=range_data_with_id.get('id'))
    assert test_delete_result is None


@mock.patch('app.models.Range.query')
def test_get_by_id(mock_query, range_data_with_id):
    """
    Test RangeService get_by_id()
    """
    range_instance = Range(**range_data_with_id)
    mock_query.get.return_value = range_instance
    test_instance = RangeService.get_by_id(range_id=range_data_with_id.get('id'))
    assert test_instance == range_instance


@mock.patch('app.models.Range.query')
def test_filter_by_range_id(mock_query, range_data_with_id):
    """
    Test RangeService filter()
    Test case when only range_id parameter is provided
    """
    range_instance = Range(**range_data_with_id)
    mock_query.filter_by.return_value.all.return_value = [range_instance]
    test_filter_result = RangeService.filter(range_id=range_data_with_id.get('id'))
    assert test_filter_result == [range_instance]


@mock.patch('app.models.Range.query')
def test_filter_by_min(mock_query, range_data_with_id):
    """
    Test RangeService filter()
    Test case when only range_min parameter is provided
    """
    range_instance = Range(**range_data_with_id)
    mock_query.filter_by.return_value.all.return_value = [range_instance]
    test_filter_result = RangeService.filter(range_min=range_data_with_id.get('min'))
    assert test_filter_result == [range_instance]


@mock.patch('app.models.Range.query')
def test_filter_by_max(mock_query, range_data_with_id):
    """
    Test RangeService filter()
    Test case when only range_max parameter is provided
    """
    range_instance = Range(**range_data_with_id)
    mock_query.filter_by.return_value.all.return_value = [range_instance]
    test_filter_result = RangeService.filter(range_max=range_data_with_id.get('max'))
    assert test_filter_result == [range_instance]


@mock.patch('app.models.Range.query')
def test_filter_by_all(mock_query, range_data_with_id):
    """
    Test RangeService filter()
    Test case when all parameters are provided
    """
    range_instance = Range(**range_data_with_id)
    mock_query.filter_by.return_value.all.return_value = [range_instance]
    test_filter_result = RangeService.filter(
        range_id=range_data_with_id.get('id'),
        range_min=range_data_with_id.get('min'),
        range_max=range_data_with_id.get('max')
    )
    assert test_filter_result == [range_instance]
