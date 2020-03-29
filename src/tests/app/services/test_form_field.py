import pytest
import mock

from app.services import FormFieldService


@mock.patch('app.schemas.FormFieldSchema')
def test_to_json(schema):
    schema.return_value = None
    result = FormFieldService.to_json(None, many=False)
    assert result == {}


@mock.patch('app.schemas.FormFieldResponseSchema')
def test_response_to_json(schema):
    schema.return_value = None
    result = FormFieldService.response_to_json(None, many=False)
    assert result == {}
