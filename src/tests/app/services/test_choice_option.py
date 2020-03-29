import pytest
import mock

from app.services import ChoiceOptionService
from app.models import ChoiceOption


@pytest.fixture()
def choice_options_data():
    data = {'field_id': 1, 'option_text': 'string1'}
    return data


@pytest.fixture()
def option_id():
    option_id = 1
    return option_id


@mock.patch('app.DB.session.add')
@mock.patch('app.services.ChoiceOptionService.filter')
def test_create(filter_mock, db_mock, choice_options_data):
    instance = ChoiceOption(**choice_options_data)
    filter_mock.return_value = None
    db_mock.return_value = None

    test_instance = ChoiceOptionService.create(**choice_options_data)

    assert instance.field_id == test_instance.field_id
    assert instance.option_text == test_instance.option_text


@mock.patch('app.services.ChoiceOptionService.filter')
def test_create_already_exist(filter_mock, choice_options_data):
    instance = ChoiceOption(**choice_options_data)
    filter_mock.return_value = [instance]

    test_instance = ChoiceOptionService.create(**choice_options_data)

    assert instance.field_id == test_instance.field_id
    assert instance.option_text == test_instance.option_text


@mock.patch("app.models.ChoiceOption.query")
def test_get_by_id(query_mock, choice_options_data, option_id):
    instance = ChoiceOption(**choice_options_data)

    query_mock.get.return_value = instance

    test_instance = ChoiceOptionService.get_by_id(option_id)

    assert test_instance == instance


@mock.patch('app.models.ChoiceOption.query')
def test_filter_by_all(query_mock, option_id, choice_options_data):
    instance = ChoiceOption(id=option_id, **choice_options_data)

    query_mock.filter_by.return_value.all.return_value = [instance]

    test_instance = ChoiceOptionService.filter(option_id=option_id, **choice_options_data)

    assert [instance] == test_instance


@mock.patch('app.models.ChoiceOption.query')
def test_filter_by_option_id(query_mock, option_id, choice_options_data):
    instance = ChoiceOption(id=option_id, **choice_options_data)

    query_mock.filter_by.return_value.all.return_value = [instance]

    test_instance = ChoiceOptionService.filter(option_id=option_id)

    assert [instance][0].id == test_instance[0].id


@mock.patch('app.models.ChoiceOption.query')
def test_filter_by_field_id(query_mock, option_id, choice_options_data):
    instance = ChoiceOption(id=option_id, **choice_options_data)

    query_mock.filter_by.return_value.all.return_value = [instance]

    test_instance = ChoiceOptionService.filter(field_id=choice_options_data.get('field_id'))

    assert [instance][0].field_id == test_instance[0].field_id


@mock.patch('app.models.ChoiceOption.query')
def test_filter_by_option_text(query_mock, option_id, choice_options_data):
    instance = ChoiceOption(id=option_id, **choice_options_data)

    query_mock.filter_by.return_value.all.return_value = [instance]

    test_instance = ChoiceOptionService.filter(option_text=choice_options_data.get('option_text'))

    assert [instance][0].option_text == test_instance[0].option_text


@mock.patch('app.services.ChoiceOptionService.get_by_id')
def test_update_not_exist(get_by_id_mock, option_id):
    get_by_id_mock.return_value = None

    test_instance = ChoiceOptionService.update(option_id=option_id)

    assert test_instance is None


@mock.patch('app.DB.session.merge')
@mock.patch('app.services.ChoiceOptionService.get_by_id')
def test_update_all_fields(get_by_id_mock, db_mock, option_id, choice_options_data):
    instance = ChoiceOption(id=option_id, **choice_options_data)
    get_by_id_mock.return_value = instance
    db_mock.return_value = None
    test_instance = ChoiceOptionService.update(option_id=option_id, **choice_options_data)

    assert test_instance == instance


@mock.patch('app.DB.session.merge')
@mock.patch('app.services.ChoiceOptionService.get_by_id')
def test_update_field_id(get_by_id_mock, db_mock, option_id, choice_options_data):
    instance = ChoiceOption(id=option_id, **choice_options_data)
    get_by_id_mock.return_value = instance
    db_mock.return_value = None
    test_instance = ChoiceOptionService.update(option_id=option_id, field_id=choice_options_data.get('field_id'))

    assert test_instance.field_id == instance.field_id


@mock.patch('app.DB.session.merge')
@mock.patch('app.services.ChoiceOptionService.get_by_id')
def test_update_option_text(get_by_id_mock, db_mock, option_id, choice_options_data):
    instance = ChoiceOption(id=option_id, **choice_options_data)
    get_by_id_mock.return_value = instance
    db_mock.return_value = None
    test_instance = ChoiceOptionService.update(option_id=option_id, option_text=choice_options_data.get('option_text'))

    assert test_instance.option_text == instance.option_text


@mock.patch('app.DB.session.delete')
@mock.patch('app.services.ChoiceOptionService.get_by_id')
def test_delete(get_by_id_mock, db_mock, option_id, choice_options_data):
    instance = ChoiceOption(id=option_id, **choice_options_data)
    get_by_id_mock.return_value = instance
    db_mock.return_value = None

    test_instance = ChoiceOptionService.delete(option_id=option_id)

    assert test_instance is True


@mock.patch('app.services.ChoiceOptionService.get_by_id')
def test_delete_not_exist(get_by_id_mock, option_id):
    get_by_id_mock.return_value = None

    test_instance = ChoiceOptionService.delete(option_id=option_id)

    assert test_instance is None


@mock.patch('app.models.ChoiceOption.query')
def test_get_by_field_and_text(query_mock, option_id, choice_options_data):
    instance = ChoiceOption(id=option_id, **choice_options_data)

    query_mock.filter_by.return_value.first.return_value = instance

    test_instance = ChoiceOptionService.get_by_field_and_text(**choice_options_data)

    assert test_instance == instance