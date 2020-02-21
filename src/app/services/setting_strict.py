"""
Setting strict service
"""
from app import DB
from app.helper.decorators import transaction_decorator
from app.helper.errors import SettingStrictNotExist
from app.models import SettingStrict


class SettingStrictService:
    """
    Setting Strict Service class
    """
    @staticmethod
    @transaction_decorator
    def create(is_strict, field_id):
        """
        Setting strict create model
        :param is_strict:
        :param field_id:
        :return:
        """
        instance = SettingStrict(is_strict=is_strict, field_id=field_id)
        DB.session.add(instance)
        return instance

    @staticmethod
    def get_by_id(setting_strict_id):
        """
        Setting strict model get by id
        :param setting_strict_id: setting strict primary key
        :return: instance of setting strict model
        """
        instance = SettingStrict.query.get(setting_strict_id)
        return instance

    @staticmethod
    def get_by_field_id(field_id):
        """
        Setting strict model get by field id
        :param field_id: field id
        :return: instance od setting strict model
        """
        instance = SettingStrict.query.filter_by(field_id=field_id).first()
        return instance

    @staticmethod
    @transaction_decorator
    def delete(setting_strict_id):
        """
        Setting strict delete model
        :param setting_strict_id:
        :return: True if deleted, or raise error if doesnt exist
        """
        instance = SettingStrictService.get_by_id(setting_strict_id)

        if instance is None:
            raise SettingStrictNotExist()
        DB.session.delete(instance)
        return True

    @staticmethod
    @transaction_decorator
    def delete_by_field_id(field_id):
        """
        Setting strict delete model by field id
        :param field_id:
        :return: True if deleted, or raise error if doesnt exist
        """
        instance = SettingStrictService.get_by_field_id(field_id)

        if instance is None:
            raise SettingStrictNotExist()
        DB.session.delete(instance)
        return True

    @staticmethod
    @transaction_decorator
    def update_strict_by_id(setting_strict_id):
        """
        Updates in instance is_strict by id
        :param setting_strict_id: Setting strict primary key
        :return: updated instance
        """
        instance = SettingStrictService.get_by_id(setting_strict_id)
        if instance is None:
            raise SettingStrictNotExist()
        instance.is_strict = not instance.is_strict
        DB.session.merge(instance)
        return instance

    @staticmethod
    @transaction_decorator
    def update_strict_by_field_id(field_id):
        """
        Updates in instance is_strict by id
        :param field_id:
        :return: updated instance
        """
        instance = SettingStrictService.get_by_field_id(field_id)
        if instance is None:
            raise SettingStrictNotExist()
        instance.is_strict = not instance.is_strict
        DB.session.merge(instance)
        return instance
