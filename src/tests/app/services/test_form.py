import pytest
import mock

from app.services import FormService
from app.schemas import FormSchema


@pytest.fixture()
def form_before_dump_data():
    data = {"id": 1, "owner_id": 1, "name": 'string', "title": 'string', "result_url": 'url@mail.com',
            "is_published": True, "created": 'date'}
    return data


@pytest.fixture()
def form_after_dump_data():
    data = {"id": 1, "ownerId": 1, "name": 'string', "title": 'string', "resultUrl": 'url@mail.com',
            "isPublished": True, "created": 'date'}
    return data


@mock.patch('app.schemas.FormSchema')
def test_to_json(schema_mock, form_before_dump_data, form_after_dump_data):
    schema_mock.return_value = FormSchema(many=False)

    test_instance = FormService.to_json(form_before_dump_data)
    assert test_instance == form_after_dump_data
