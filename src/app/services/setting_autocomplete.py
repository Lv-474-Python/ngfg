from app.models import SettingAutocomplete
from app import DB
from sqlalchemy.exc import IntegrityError


class SettingAutocompleteService:

    @staticmethod
    def create(data_url, sheet, from_row, to_row, field_id):
        DB.session.begin(subtransactions=True)

        setting_autocomplete = SettingAutocomplete(
            data_url=data_url,
            sheet=sheet,
            from_row=from_row,
            to_row=to_row,
            field_id=field_id
        )
        try:
            DB.session.add(setting_autocomplete)
            DB.session.commit()

        except IntegrityError:
            DB.session.rollback()
            raise
        
        return setting_autocomplete

    @staticmethod
    def update(setting_autocomplete_id, data_url=None, sheet=None, from_row=None, to_row=None, field_id=None):
        DB.session.begin(subtransactions=True)

        setting_autocomplete = SettingAutocomplete.query.get(setting_autocomplete_id)

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

        try:
            DB.session.merge(setting_autocomplete)
            DB.session.commit()
        except IntegrityError:
            DB.session.rollback()
            raise

        return setting_autocomplete

    @staticmethod
    def delete(setting_autocomplete_id):
        DB.session.begin(subtransactions=True)

        setting_autocomplete = SettingAutocomplete.query.get(setting_autocomplete_id)

        try:
            DB.session.delete(setting_autocomplete)
            DB.session.commit()
        except IntegrityError:
            DB.session.rollback()
            raise

        return True
