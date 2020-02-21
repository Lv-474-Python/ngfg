"""
Form operations.
"""

from app import DB
from app.helper.errors import FormNotExist
from app.models import Form
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
        :return:
        """
        form = FormService.form_filter(owner_id=owner_id,
                                       name=name,
                                       title=title,
                                       result_url=result_url,
                                       is_published=is_published)

        print(form)
        if form:
            return form

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
    def update(form_id, owner_id=None, name=None, title=None, result_url=None,
               is_published=None):
        """
        Update form in database

        :param form_id:
        :param owner_id:
        :param name:
        :param title:
        :param result_url:
        :param is_published:
        :return:
        """
        form = FormService.get_by_id(form_id)

        if not form:
            raise FormNotExist()

        if owner_id:
            form.owner_id = owner_id

        if name:
            form.name = name

        if title:
            form.title = title

        if result_url:
            form.result_url = result_url

        if is_published:
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
    def form_filter(owner_id=None, name=None, title=None, result_url=None,
                    is_published=None):
        """
        Filter form from database by arguments

        :param owner_id:
        :param name:
        :param title:
        :param result_url:
        :param is_published:
        :return: list of forms
        """

        data = {}

        if owner_id:
            data['owner_id'] = owner_id

        if name:
            data['name'] = name

        if title:
            data['title'] = title

        if result_url:
            data['result_url'] = result_url

        if is_published:
            data['is_published'] = is_published

        form = Form.query.filter_by(**data).all()

        # if we raise error we wont create new form
        if not form:
            return None

        return form
