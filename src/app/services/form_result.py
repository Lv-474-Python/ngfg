from app.models import FormResult
from app import DB
from sqlalchemy.exc import IntegrityError


class FormResultService:
    @staticmethod
    def create(user_id, form_id, answer):
        DB.session.begin(subtransactions=True)

        form_result = FormResult(user_id=user_id, answer=answer, form_id=form_id)

        try:
            DB.session.add(form_result)
            DB.session.commit()
        except IntegrityError:
            DB.session.rollback()
            raise
        return form_result
