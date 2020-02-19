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

    @staticmethod
    def update(form_result_id, user_id=None, form_id=None, answer=None):
        DB.session.begin(subtransactions=True)

        form_result = FormResult.query.get(form_result_id)

        if user_id is not None:
            form_result.user_id = user_id
        if form_id is not None:
            form_result.form_id = form_id
        if answer is not None:
            form_result.answer = answer

        try:
            DB.session.merge(form_result)
            DB.session.commit()
        except IntegrityError:
            DB.session.rollback()
            raise

        return form_result

    @staticmethod
    def delete(form_result_id):
        DB.session.begin(subtransactions=True)

        form_result = FormResult.query.get(form_result_id)

        try:
            DB.session.delete(form_result)
            DB.session.commit()
        except IntegrityError:
            DB.session.rollback()
            raise
        return True
