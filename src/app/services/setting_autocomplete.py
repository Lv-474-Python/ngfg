"""
SettingAutocomplete service
"""

from app.models import SettingAutocomplete
from app import DB
from app.helper.decorators import transaction_decorator
from app.helper.errors import SettingAutocompleteNotExist


class SettingAutocompleteService:
    """
    Class for SettingAutocomplete model
    """

    @staticmethod
    @transaction_decorator
    def create(data_url, sheet, from_row, to_row, field_id):
        """
        Create SettingAutocomplete model

        :param data_url:
        :param sheet:
        :param from_row:
        :param to_row:
        :param field_id:
        :return: setting_autocomplete or None
        """
        setting_autocomplete = SettingAutocomplete(
            data_url=data_url,
            sheet=sheet,
            from_row=from_row,
            to_row=to_row,
            field_id=field_id
        )
        DB.session.add(setting_autocomplete)
        return setting_autocomplete

    @staticmethod
    @transaction_decorator
    def update(setting_autocomplete_id,  # pylint: disable=too-many-arguments
               data_url=None,
               sheet=None,
               from_row=None,
               to_row=None,
               field_id=None):
        """
        Update SettingAutocomplete model

        :param setting_autocomplete_id: required param
        :param data_url:
        :param sheet:
        :param from_row:
        :param to_row:
        :param field_id:
        :return: updated model or None
        """
        setting_autocomplete = SettingAutocompleteService.get_by_id(setting_autocomplete_id)

        if setting_autocomplete is None:
            raise SettingAutocompleteNotExist

        if data_url is not None:
            setting_autocomplete.data_url = data_url
        if sheet is not None:
            setting_autocomplete.sheet = sheet
        if from_row is not None:
            setting_autocomplete.from_row = from_row
        if to_row is not None:
            setting_autocomplete.to_row = to_row
        if field_id is not None:
            setting_autocomplete.field_id = field_id

        DB.session.merge(setting_autocomplete)

        return setting_autocomplete

    @staticmethod
    @transaction_decorator
    def delete(setting_autocomplete_id):
        """
        Delete SettingAutocomplete model by id

        :param setting_autocomplete_id:
        :return: True if model is deleted or None
        """
        setting_autocomplete = SettingAutocompleteService.get_by_id(setting_autocomplete_id)

        if setting_autocomplete is None:
            raise SettingAutocompleteNotExist
        DB.session.delete(setting_autocomplete)

        return True

    @staticmethod
    def get_by_id(setting_autocomplete_id):
        """
        Get SettingAutocomplete model by id

        :param setting_autocomplete_id:
        :return: SettingAutocomplete object or None
        """
        setting_autocomplete = SettingAutocomplete.query.get(setting_autocomplete_id)
        return setting_autocomplete

    @staticmethod
    def filter(setting_autocomplete_id=None,  # pylint: disable=too-many-arguments
               data_url=None,
               sheet=None,
               from_row=None,
               to_row=None,
               field_id=None):
        """
        SettingAutocomplete filter method

        :param setting_autocomplete_id:
        :param data_url:
        :param sheet:
        :param from_row:
        :param to_row:
        :param field_id:
        :return: list of SettingAutocomplete objects or empty list
        """
        filter_data = {}

        if setting_autocomplete_id is not None:
            filter_data['id'] = setting_autocomplete_id
        if data_url is not None:
            filter_data['data_url'] = data_url
        if sheet is not None:
            filter_data['sheet'] = sheet
        if from_row is not None:
            filter_data['from_row'] = from_row
        if to_row is not None:
            filter_data['to_row'] = to_row
        if field_id is not None:
            filter_data['field_id'] = field_id

        result = SettingAutocomplete.query.filter_by(**filter_data).all()
        return result
