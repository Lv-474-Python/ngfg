"""
Form operations.
"""

from app import DB
from app.helper.errors import FormNotExist
from app.models import Form, FormSchema
from app.helper.decorators import transaction_decorator


class FormService:
    """
    Class with form operations
    """

    @staticmethod
    @transaction_decorator
    def create(owner_id, name, title, result_url, is_published):
        """
        Create new form in database

        :param owner_id: User who created the form
        :param name: Name, which is visible only for the owner, for searching
        :param title: Form title visible for all users
        :param result_url: Url for the domain where form result are stored
        :param is_published: is form published or not
        :return: form or None
        """
        form = Form(owner_id=owner_id,
                    name=name,
                    title=title,
                    result_url=result_url,
                    is_published=is_published)
        DB.session.add(form)
        return form

    @staticmethod
    @transaction_decorator
    def get_by_id(form_id):
        """
        Get form by id

        :param id:
        :return: form or none
        """
        form = Form.query.get(form_id)
        return form

    @staticmethod
    @transaction_decorator
    def update(form_id, # pylint: disable=too-many-arguments
               owner_id=None,
               name=None,
               title=None,
               result_url=None,
               is_published=None):
        """
        Update form in database

        :param form_id: from id
        :param owner_id: User who created the form
        :param name: Name, which is visible only for the owner, for searching
        :param title: Form title visible for all users
        :param result_url: Url for the domain where form result are stored
        :param is_published: is form published or not
        :return: form or None
        """
        form = FormService.get_by_id(form_id)

        if form is None:
            raise FormNotExist()

        if owner_id is not None:
            form.owner_id = owner_id
        if name is not None:
            form.name = name
        if title is not None:
            form.title = title
        if result_url is not None:
            form.result_url = result_url
        if is_published is not None:
            form.is_published = is_published

        DB.session.merge(form)
        return form

    @staticmethod
    @transaction_decorator
    def delete(form_id):
        """
        Delete form from database

        :param form_id:
        :return: True or None
        """
        form = FormService.get_by_id(form_id)

        if form is None:
            raise FormNotExist()

        DB.session.delete(form)
        return True

    @staticmethod
    @transaction_decorator
    def filter(owner_id=None,
               name=None,
               title=None,
               result_url=None,
               is_published=None):
        """
        Filter form from database by arguments

        :param owner_id: User who created the form
        :param name: Name, which is visible only for the owner, for searching
        :param title: Form title visible for all users
        :param result_url: Url for the domain where form result are stored
        :param is_published: is form published or not
        :return: list of forms
        """

        data = {}

        if owner_id is not None:
            data['owner_id'] = owner_id
        if name is not None:
            data['name'] = name
        if title is not None:
            data['title'] = title
        if result_url is not None:
            data['result_url'] = result_url
        if is_published is not None:
            data['is_published'] = is_published

        forms = Form.query.filter_by(**data).all()

        return forms

    @staticmethod
    def to_json(data, many=False):
        """
        Get data in json format
        """
        schema = FormSchema(many=many)
        return schema.dump(data)

    @staticmethod
    def validate_data(data):
        """
        Validate data by FormSchema
        """
        schema = FormSchema()
        errors = schema.validate(data)
        return (not bool(errors), errors)
