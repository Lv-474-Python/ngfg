import pytest
import mock

from app.services import FormFieldService
from app.models import FormField


@pytest.fixture()
def form_field_data():
    data = {'form_id': 1, 'field_id': 1, 'question': 'string', 'position': 1}
    return data


@pytest.fixture()
def form_field_id():
    form_field_id = 1
    return form_field_id


@pytest.fixture()
def form_field_updated_data():
    data = {'form_id': 2, 'field_id': 2, 'question': 'new_string', 'position': 2}
    return data


@mock.patch('app.DB.session.add')
@mock.patch('app.helper.redis_manager.RedisManager.get')
def test_create(redis_manager_get_mock, db_mock, form_field_data):
    db_mock.return_value = None
    redis_manager_get_mock.return_value = [FormField(**form_field_data), FormField(**form_field_data)]

    instance = FormField(**form_field_data)
    test_instance = FormFieldService.create(**form_field_data)

    assert instance.form_id == test_instance.form_id
    assert instance.field_id == test_instance.field_id
    assert instance.question == test_instance.question
    assert instance.position == test_instance.position


@mock.patch('app.models.FormField.query')
@mock.patch('app.helper.redis_manager.RedisManager.get')
def test_get_by_id(redis_manager_get_mock, query_mock, form_field_data):
    instance = FormField(**form_field_data)

    redis_manager_get_mock.return_value = None
    query_mock.get.return_value = instance

    test_instance = FormFieldService.get_by_id(1)

    assert instance == test_instance


@mock.patch('app.helper.redis_manager.RedisManager.set')
@mock.patch('app.models.FormField.query')
@mock.patch('app.helper.redis_manager.RedisManager.get')
@mock.patch('app.helper.redis_manager.RedisManager.generate_key')
def test_filter_by_all_no_redis_result(
        generate_key_mock,
        redis_manager_get_mock,
        query_mock,
        redis_manager_set_mock,
        form_field_data):
    instance = FormField(**form_field_data)

    generate_key_mock.return_value = 'form_fields:form_id:1field_id:1position:1question:string'
    redis_manager_get_mock.return_value = None
    query_mock.filter_by.return_value.all.return_value = [instance]
    redis_manager_set_mock.return_value = None

    test_instance = FormFieldService.filter(**form_field_data)

    assert test_instance == [instance]


@mock.patch('app.helper.redis_manager.RedisManager.set')
@mock.patch('app.models.FormField.query')
@mock.patch('app.helper.redis_manager.RedisManager.get')
@mock.patch('app.helper.redis_manager.RedisManager.generate_key')
def test_filter_by_form_id_no_redis_result(
        generate_key_mock,
        redis_manager_get_mock,
        query_mock,
        redis_manager_set_mock,
        form_field_data):
    instance = FormField(**form_field_data)

    generate_key_mock.return_value = 'form_fields:form_id:1'
    redis_manager_get_mock.return_value = None
    query_mock.filter_by.return_value.all.return_value = [instance]
    redis_manager_set_mock.return_value = None

    test_instance = FormFieldService.filter(form_id=form_field_data.get('form_id'))

    assert test_instance[0].form_id == [instance][0].form_id


@mock.patch('app.helper.redis_manager.RedisManager.set')
@mock.patch('app.models.FormField.query')
@mock.patch('app.helper.redis_manager.RedisManager.get')
@mock.patch('app.helper.redis_manager.RedisManager.generate_key')
def test_filter_by_field_id_no_redis_result(
        generate_key_mock,
        redis_manager_get_mock,
        query_mock,
        redis_manager_set_mock,
        form_field_data):
    instance = FormField(**form_field_data)

    generate_key_mock.return_value = 'form_fields:field_id:1'
    redis_manager_get_mock.return_value = None
    query_mock.filter_by.return_value.all.return_value = [instance]
    redis_manager_set_mock.return_value = None

    test_instance = FormFieldService.filter(field_id=form_field_data.get('field_id'))

    assert test_instance[0].field_id == [instance][0].field_id


@mock.patch('app.helper.redis_manager.RedisManager.set')
@mock.patch('app.models.FormField.query')
@mock.patch('app.helper.redis_manager.RedisManager.get')
@mock.patch('app.helper.redis_manager.RedisManager.generate_key')
def test_filter_by_question_no_redis_result(
        generate_key_mock,
        redis_manager_get_mock,
        query_mock,
        redis_manager_set_mock,
        form_field_data):
    instance = FormField(**form_field_data)

    generate_key_mock.return_value = 'form_fields:question:string'
    redis_manager_get_mock.return_value = None
    query_mock.filter_by.return_value.all.return_value = [instance]
    redis_manager_set_mock.return_value = None

    test_instance = FormFieldService.filter(question=form_field_data.get('question'))

    assert test_instance[0].question == [instance][0].question


@mock.patch('app.helper.redis_manager.RedisManager.set')
@mock.patch('app.models.FormField.query')
@mock.patch('app.helper.redis_manager.RedisManager.get')
@mock.patch('app.helper.redis_manager.RedisManager.generate_key')
def test_filter_by_position_no_redis_result(
        generate_key_mock,
        redis_manager_get_mock,
        query_mock,
        redis_manager_set_mock,
        form_field_data):
    instance = FormField(**form_field_data)

    generate_key_mock.return_value = 'form_fields:position:1'
    redis_manager_get_mock.return_value = None
    query_mock.filter_by.return_value.all.return_value = [instance]
    redis_manager_set_mock.return_value = None

    test_instance = FormFieldService.filter(position=form_field_data.get('position'))

    assert test_instance[0].position == [instance][0].position


@mock.patch('app.helper.redis_manager.RedisManager.get')
@mock.patch('app.DB.session.merge')
@mock.patch('app.services.FormFieldService.get_by_id')
def test_update_all(get_by_id_mock,
                    db_mock,
                    redis_manager_get_mock,
                    form_field_id,
                    form_field_data,
                    form_field_updated_data):
    instance = FormField(**form_field_data)
    updated_instance = FormField(**form_field_updated_data)

    get_by_id_mock.return_value = instance
    db_mock.return_value = None
    redis_manager_get_mock.return_value = True

    test_instance = FormFieldService.update(form_field_id, **form_field_updated_data)

    assert updated_instance.form_id == test_instance.form_id
    assert updated_instance.field_id == test_instance.field_id
    assert updated_instance.question == test_instance.question
    assert updated_instance.position == test_instance.position


@mock.patch('app.helper.redis_manager.RedisManager.get')
@mock.patch('app.DB.session.merge')
@mock.patch('app.services.FormFieldService.get_by_id')
def test_update_form_id(get_by_id_mock,
                        db_mock,
                        redis_manager_get_mock,
                        form_field_id,
                        form_field_data,
                        form_field_updated_data):
    instance = FormField(**form_field_data)
    updated_instance = FormField(**form_field_updated_data)
    get_by_id_mock.return_value = instance
    db_mock.return_value = None
    redis_manager_get_mock.return_value = True

    test_instance = FormFieldService.update(form_field_id, form_id=form_field_updated_data.get('form_id'))

    assert updated_instance.form_id == test_instance.form_id
    assert updated_instance.field_id != test_instance.field_id
    assert updated_instance.question != test_instance.question
    assert updated_instance.position != test_instance.position


@mock.patch('app.helper.redis_manager.RedisManager.get')
@mock.patch('app.DB.session.merge')
@mock.patch('app.services.FormFieldService.get_by_id')
def test_update_field_id(get_by_id_mock,
                         db_mock,
                         redis_manager_get_mock,
                         form_field_id,
                         form_field_data,
                         form_field_updated_data):
    instance = FormField(**form_field_data)
    updated_instance = FormField(**form_field_updated_data)
    get_by_id_mock.return_value = instance
    db_mock.return_value = None
    redis_manager_get_mock.return_value = True

    test_instance = FormFieldService.update(form_field_id, field_id=form_field_updated_data.get('field_id'))

    assert updated_instance.form_id != test_instance.form_id
    assert updated_instance.field_id == test_instance.field_id
    assert updated_instance.question != test_instance.question
    assert updated_instance.position != test_instance.position


@mock.patch('app.helper.redis_manager.RedisManager.get')
@mock.patch('app.DB.session.merge')
@mock.patch('app.services.FormFieldService.get_by_id')
def test_update_question(get_by_id_mock,
                         db_mock,
                         redis_manager_get_mock,
                         form_field_id,
                         form_field_data,
                         form_field_updated_data):
    instance = FormField(**form_field_data)
    updated_instance = FormField(**form_field_updated_data)
    get_by_id_mock.return_value = instance
    db_mock.return_value = None
    redis_manager_get_mock.return_value = True

    test_instance = FormFieldService.update(form_field_id, question=form_field_updated_data.get('question'))

    assert updated_instance.form_id != test_instance.form_id
    assert updated_instance.field_id != test_instance.field_id
    assert updated_instance.question == test_instance.question
    assert updated_instance.position != test_instance.position


@mock.patch('app.helper.redis_manager.RedisManager.get')
@mock.patch('app.DB.session.merge')
@mock.patch('app.services.FormFieldService.get_by_id')
def test_update_position(get_by_id_mock,
                         db_mock,
                         redis_manager_get_mock,
                         form_field_id,
                         form_field_data,
                         form_field_updated_data):
    instance = FormField(**form_field_data)
    updated_instance = FormField(**form_field_updated_data)
    get_by_id_mock.return_value = instance
    db_mock.return_value = None
    redis_manager_get_mock.return_value = True

    test_instance = FormFieldService.update(form_field_id, position=form_field_updated_data.get('position'))

    assert updated_instance.form_id != test_instance.form_id
    assert updated_instance.field_id != test_instance.field_id
    assert updated_instance.question != test_instance.question
    assert updated_instance.position == test_instance.position


@mock.patch('app.services.FormFieldService.get_by_id')
def test_update_with_form_field_not_exist(get_by_id_mock, form_field_id):
    get_by_id_mock.return_value = None

    test_instance = FormFieldService.update(form_field_id)

    assert test_instance == None
