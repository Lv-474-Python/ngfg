import pytest
import mock

from app.services import ChoiceOptionService
from app.models import ChoiceOption


@pytest.fixture()
def choice_options_date():
    data = {'field_id': 1, 'option_text': 'string1'}
    return data


@mock.patch('app.DB.session.add')
@mock.patch('app.services.ChoiceOptionService.filter')
def test_create(filter_mock, db_mock, choice_options_date):
    instance = ChoiceOption(**choice_options_date)
    filter_mock.return_value = None
    db_mock.return_value = None

    test_instance = ChoiceOptionService.create(**choice_options_date)

    assert instance.field_id == test_instance.field_id
    assert instance.option_text == test_instance.option_text