"""
Test UserService
"""

import mock
import pytest

from app.models import Form
from app.services import FormService

from services_test_data import (
    FORM_SERVICE_CREATE_DATA,
    FORM_SERVICE_GET_BY_ID_DATA,
    FORM_SERVICE_UPDATE_DATA,
    FORM_SERVICE_UPDATE_ERROR_DATA,
    FORM_SERVICE_DELETE_DATA,
    FORM_SERVICE_DELETE_ERROR_DATA,
    FORM_SERVICE_FILTER_BY_FORM_ID_DATA,
    FORM_SERVICE_FILTER_BY_OWNER_ID_DATA,
    FORM_SERVICE_FILTER_BY_NAME_DATA,
    FORM_SERVICE_FILTER_BY_TITLE_DATA,
    FORM_SERVICE_FILTER_BY_RESULT_URL_DATA,
    FORM_SERVICE_FILTER_BY_IS_PUBLISHED_DATA,
    FORM_SERVICE_FILTER_BY_ALL_DATA
)


# create
@pytest.mark.parametrize(
    "owner_id, name, title, result_url, is_published",
    FORM_SERVICE_CREATE_DATA
)
@mock.patch("app.DB.session.add")
def test_create(
        mock_db_add,
        owner_id,
        name,
        title,
        result_url,
        is_published):
    """
    Test FormService create()
    Test case when executed successfully
    """
    form = Form(
        owner_id=owner_id,
        name=name,
        title=title,
        result_url=result_url,
        is_published=is_published
    )

    mock_db_add.return_value = form

    result = FormService.create(owner_id, name, title, result_url, is_published)

    assert result.owner_id == form.owner_id
    assert result.name == form.name
    assert result.title == form.title
    assert result.result_url == form.result_url
    assert result.is_published == form.is_published


# get_by_id
@pytest.mark.parametrize(
    "form_id, owner_id, name, title, result_url, is_published",
    FORM_SERVICE_GET_BY_ID_DATA
)
@mock.patch("app.models.Form.query")
def test_get_by_id(
        mock_form_query,
        form_id,
        owner_id,
        name,
        title,
        result_url,
        is_published):
    """
    Test FormService get_by_id()
    Test case when method executed successfully
    """
    form = Form(
        owner_id=owner_id,
        name=name,
        title=title,
        result_url=result_url,
        is_published=is_published
    )

    mock_form_query.get.return_value = form

    result = FormService.get_by_id(form_id)

    assert result.owner_id == form.owner_id
    assert result.name == form.name
    assert result.title == form.title
    assert result.result_url == form.result_url
    assert result.is_published == form.is_published


# update
@pytest.fixture()
def form():
    form = Form(
        owner_id=1,
        name="form name",
        title="form title",
        result_url="http://docs.google.com/spreadsheet/d/asdsa",
        is_published=True
    )
    return form

@pytest.mark.parametrize(
    "form_id, owner_id, name, title, result_url, is_published",
    FORM_SERVICE_UPDATE_DATA
)
@mock.patch("app.DB.session.merge")
@mock.patch("app.services.FormService.get_by_id")
def test_update(
        mock_form_get,
        mock_db_merge,
        form,
        form_id,
        owner_id,
        name,
        title,
        result_url,
        is_published):
    """
    Test FormService update()
    Test case when method executed successfully
    """
    mock_form_get.return_value = form
    mock_db_merge.return_value = None

    updated_owner_id = owner_id if owner_id is not None else form.owner_id
    updated_name = name if name is not None else form.name
    updated_title = title if title is not None else form.title
    updated_result_url = result_url if result_url is not None else form.result_url
    updated_is_published = is_published if is_published is not None else form.is_published

    result = FormService.update(form_id, owner_id, name, title, result_url, is_published)

    assert result.owner_id == updated_owner_id
    assert result.name == updated_name
    assert result.title == updated_title
    assert result.result_url == updated_result_url
    assert result.is_published == updated_is_published


@pytest.mark.parametrize(
    "form_id",
    FORM_SERVICE_UPDATE_ERROR_DATA
)
@mock.patch("app.services.FormService.get_by_id")
def test_update_error(mock_form_get, form_id):
    """
    Test FormService update()
    Test case when method raised FormNotExist and returned None
    """
    mock_form_get.return_value = None

    result = FormService.update(form_id)

    assert result is None


# delete
@pytest.mark.parametrize(
    "form_id",
    FORM_SERVICE_DELETE_DATA
)
@mock.patch("app.DB.session.delete")
@mock.patch("app.services.FormService.get_by_id")
def test_delete(mock_form_get, mock_db_delete, form, form_id):
    """
    Test FormService delete()
    Test case when method executed successfully
    """
    mock_form_get.return_value = form
    mock_db_delete.return_value = None

    result = FormService.delete(form_id)

    assert result == True


@pytest.mark.parametrize(
    "form_id",
    FORM_SERVICE_DELETE_ERROR_DATA
)
@mock.patch("app.services.FormService.get_by_id")
def test_delete_error(mock_form_get, form_id):
    """
    Test FormService delete()
    Test case when method raised FormNotExist and returned None
    """
    mock_form_get.return_value = None

    result = FormService.delete(form_id)

    assert result is None


# filter
@pytest.mark.parametrize(
    "form_id",
    FORM_SERVICE_FILTER_BY_FORM_ID_DATA
)
@mock.patch("app.models.Form.query")
def test_filter_by_form_id(mock_form_query, form, form_id):
    """
    Test FormService filter()
    Test case when method filtered just by form_id
    """
    form.form_id = form_id

    mock_form_query.filter_by().all.return_value = [form]

    result = FormService.filter(form_id=form_id)

    assert result == [form]


@pytest.mark.parametrize(
    "owner_id",
    FORM_SERVICE_FILTER_BY_OWNER_ID_DATA
)
@mock.patch("app.models.Form.query")
def test_filter_by_owner_id(mock_form_query, form, owner_id):
    """
    Test FormService filter()
    Test case when method filtered just by owner_id
    """
    form.owner_id = owner_id

    mock_form_query.filter_by().all.return_value = [form]

    result = FormService.filter(owner_id=owner_id)

    assert result == [form]


@pytest.mark.parametrize(
    "name",
    FORM_SERVICE_FILTER_BY_NAME_DATA
)
@mock.patch("app.models.Form.query")
def test_filter_by_name(mock_form_query, form, name):
    """
    Test FormService filter()
    Test case when method filtered just by name
    """
    form.name = name

    mock_form_query.filter_by().all.return_value = [form]

    result = FormService.filter(name=name)

    assert result == [form]


@pytest.mark.parametrize(
    "title",
    FORM_SERVICE_FILTER_BY_TITLE_DATA
)
@mock.patch("app.models.Form.query")
def test_filter_by_title(mock_form_query, form, title):
    """
    Test FormService filter()
    Test case when method filtered just by title
    """
    form.title = title

    mock_form_query.filter_by().all.return_value = [form]

    result = FormService.filter(title=title)

    assert result == [form]


@pytest.mark.parametrize(
    "result_url",
    FORM_SERVICE_FILTER_BY_RESULT_URL_DATA
)
@mock.patch("app.models.Form.query")
def test_filter_by_result_url(mock_form_query, form, result_url):
    """
    Test FormService filter()
    Test case when method filtered just by result_url
    """
    form.result_url = result_url

    mock_form_query.filter_by().all.return_value = [form]

    result = FormService.filter(result_url=result_url)

    assert result == [form]


@pytest.mark.parametrize(
    "is_published",
    FORM_SERVICE_FILTER_BY_IS_PUBLISHED_DATA
)
@mock.patch("app.models.Form.query")
def test_filter_by_is_published(mock_form_query, form, is_published):
    """
    Test FormService filter()
    Test case when method filtered just by is_published
    """
    form.is_published = is_published

    mock_form_query.filter_by().all.return_value = [form]

    result = FormService.filter(is_published=is_published)

    assert result == [form]


@pytest.mark.parametrize(
    "form_id, owner_id, name, title, result_url, is_published",
    FORM_SERVICE_FILTER_BY_ALL_DATA
)
@mock.patch("app.models.Form.query")
def test_filter_by_all(
        mock_form_query,
        form,
        form_id,
        owner_id,
        name,
        title,
        result_url,
        is_published):
    """
    Test FormService filter()
    Test case when method filtered just by form_id, owner_id, name, title, result_url, is_published
    """
    form = Form(
        owner_id=owner_id,
        name=name,
        title=title,
        result_url=result_url,
        is_published=is_published
    )

    mock_form_query.filter_by().all.return_value = [form]

    result = FormService.filter(
        form_id=form_id,
        owner_id=owner_id,
        name=name,
        title=title,
        result_url=result_url,
        is_published=is_published
    )

    assert result == [form]
