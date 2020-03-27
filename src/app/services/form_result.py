"""
FormResult service
"""

from app.helper.answer_validation import is_numeric
from app.helper.constants import MAX_TEXT_LENGTH, MIN_POSTGRES_INT, MAX_POSTGRES_INT
from app.helper.enums import FieldType
from app.helper.redis_manager import RedisManager
from app.models import FormResult, Range
from app import DB
from app.helper.decorators import transaction_decorator
from app.schemas import FormResultPostSchema, FormResultGetSchema
from app.services.field import FieldService
from app.services.form_field import FormFieldService


class FormResultService:
    """
    Class for FormResult service
    """

    @staticmethod
    @transaction_decorator
    def create(user_id, form_id, answers):
        """
        Create FormResult model

        :param user_id:
        :param form_id:
        :param answers:
        :return: FormResult object or None
        """

        form_result = FormResult(
            user_id=user_id,
            form_id=form_id,
            answers=answers
        )

        DB.session.add(form_result)

        key = f'form_results:form_id:{form_id}'
        result = RedisManager.get(key, 'data')
        if result is not None:
            RedisManager.delete(key)

        return form_result

    @staticmethod
    def get_by_id(form_result_id):
        """
        Get FormResult model by id

        :param form_result_id:
        :return: FormResult object or None
        """
        result = RedisManager.get(f'form_result:{form_result_id}', 'data')

        if result is None:
            result = FormResult.query.get(form_result_id)
            if result is not None:
                RedisManager.set(f'form_result:{form_result_id}', result)

        return result

    @staticmethod
    def filter(form_result_id=None, user_id=None, form_id=None, answers=None, created=None):
        """
        FormResult filter method

        :param form_result_id:
        :param user_id:
        :param form_id:
        :param answers:
        :param created:
        :return: list of FormResult objects or empty list
        """
        filter_data = {}

        if form_result_id is not None:
            filter_data['id'] = form_result_id
        if user_id is not None:
            filter_data['user_id'] = user_id
        if form_id is not None:
            filter_data['form_id'] = form_id
        if answers is not None:
            filter_data['answers'] = answers
        if created is not None:
            filter_data['created'] = created

        key = RedisManager.generate_key('form_results:', filter_data)
        result = RedisManager.get(key, 'data')

        if result is None:
            result = FormResult.query.filter_by(**filter_data).all()
            RedisManager.set(key, result)

        return result

    @staticmethod
    def to_json(data, many=False):
        """
        Get data in json format
        """
        schema = FormResultGetSchema(many=many)
        result = schema.dump(data)
        return result

    @staticmethod
    def _validate_answers_positions(form_result):
        """
        Method for comparing positions, passed in JSON answers with DB

        :param form_result:
        :return: True if positions matching, else False
        """
        form_fields = FormFieldService.filter(form_id=form_result["form_id"])
        if len(form_fields) != len(form_result["answers"]):
            return False, {"Amount": "Wrong answers amount"}
        for form_field in form_fields:
            for answer in form_result["answers"]:
                if form_field.position == answer["position"]:
                    break
            else:
                return False, {"Positions": "Wrong positions"}
        return True, {}

    @staticmethod
    def _validate_answers(form_result):
        """

        :param form_result:
        :return:
        """
        errors = {}
        form_fields = FormFieldService.filter(form_id=form_result["form_id"])
        for answer in form_result["answers"]:
            field_id = [form_field.field_id
                        for form_field in form_fields
                        if form_field.position == answer["position"]][0]
            field = FieldService.get_by_id(field_id)
            options = FieldService.get_additional_options(
                field.id,
                field.field_type
            )

            if field.field_type == FieldType.Number.value:
                FormResultService._check_number_field(field, options, answer, errors)
            elif field.field_type == FieldType.Text.value:
                FormResultService._check_text_field(field, options, answer, errors)
            elif field.field_type == FieldType.Checkbox.value:
                FormResultService._check_checkbox_field(field, options, answer, errors)
            elif field.field_type == FieldType.Radio.value:
                FormResultService._check_radio_field(options, answer, errors)
            elif field.field_type == FieldType.TextArea.value:
                pass
            elif field.field_type == FieldType.Autocomplete.value:
                FormResultService._check_autocomplete_field(options, answer, errors)

        return [not bool(errors), errors]

    @staticmethod
    def _check_autocomplete_field(options, answer, errors):
        """

        :param options:
        :param answer:
        :param errors:
        :return:
        """
        if not isinstance(answer['answer'], str):
            errors[answer["position"]] = "Must be string."
            return False

        if str(answer['answer']) not in options['values']:
            errors[answer["position"]] = "No such choice in this field."
            return False
        return True

    @staticmethod
    def _check_radio_field(options, answer, errors):
        """

        :param options:
        :param answer:
        :param errors:
        :return:
        """
        radio_answer = answer["answer"]
        if not isinstance(radio_answer, list):
            errors[answer["position"]] = "Must be list."
            return False

        if len(radio_answer) != 1:
            errors[answer["position"]] = "Must be exactly one choice."
            return False

        radio_answer = str(radio_answer[0])
        if radio_answer not in options['choiceOptions']:
            errors[answer["position"]] = "No such choice in this field."
            return False
        return True

    @staticmethod
    def _check_checkbox_field(field, options, answer, errors):
        """

        :param field:
        :param options:
        :param answer:
        :param errors:
        :return:
        """
        answers = answer["answer"]
        if not isinstance(answers, list):
            errors[answer["position"]] = "Answers must be list type."
            return False
        answers = list(set(answers))  # Remove all repeating answers

        if options['range']['min'] is None and options['range']['max'] is None:
            field.range = Range(min=0, max=len(options['choiceOptions']))
        elif options['range']['min'] is None and options['range']['max'] is not None:
            field.range = Range(min=0, max=options['range']['max'])
        elif options['range']['min'] is not None and options['range']['max'] is None:
            field.range = Range(min=options['range']['min'], max=len(options['choiceOptions']))
        else:
            field.range = Range(min=options['range']['min'], max=options['range']['max'])

        if not field.range.min <= len(answers) <= field.range.max:
            errors[answer["position"]] = "Answers amount out of range."
            return False

        wrong_answers = []

        for ans in answers:
            if ans not in options['choiceOptions']:
                wrong_answers.append(ans)

        if len(wrong_answers) > 0:
            errors[answer["position"]] = 'There is no '
            for ans in wrong_answers:
                errors[answer["position"]] += ans + '; '
            errors[answer["position"]] += 'in possible choices.'
            return False
        return True

    @staticmethod
    def _check_number_field(field, options, answer, errors):
        """

        :param field:
        :param answer:
        :param options:
        :param errors:
        :return:
        """
        if not is_numeric(answer["answer"]):
            errors[answer["position"]] = "Value is not numeric"
            return False
        answer["answer"] = float(answer["answer"])

        if field.is_strict:
            if int(answer["answer"]) != answer["answer"]:
                errors[answer["position"]] = "Value is not strict number"
                return False

        if options['range']['min'] is None and options['range']['max'] is None:
            field.range = Range(min=MIN_POSTGRES_INT, max=MAX_POSTGRES_INT)
        elif options['range']['min'] is None and options['range']['max'] is not None:
            field.range = Range(min=MIN_POSTGRES_INT, max=options['range']['max'])
        elif options['range']['max'] is None and options['range']['min'] is not None:
            field.range = Range(min=options['range']['min'], max=MAX_POSTGRES_INT)
        else:
            field.range = Range(min=options['range']['min'], max=options['range']['max'])

        if not field.range.min <= answer["answer"] <= field.range.max:
            errors[answer["position"]] = "Value is out of range!"
            return False
        return True

    @staticmethod
    def _check_text_field(field, options, answer, errors):
        """

        :param field:
        :param options:
        :param answer:
        :param errors:
        :return:
        """
        if field.is_strict:
            if not str(answer["answer"]).isalpha():
                errors[answer["position"]] = "Value is not strict text"
                return False

        if options['range']['min'] is None and options['range']['max'] is None:
            field.range = Range(min=0, max=MAX_TEXT_LENGTH)
        elif options['range']['min'] is None and options['range']['max'] is not None:
            field.range = Range(min=0, max=options['range']['max'])
        elif options['range']['max'] is None and options['range']['max'] is not None:
            field.range = Range(min=options['range']['min'], max=MAX_TEXT_LENGTH)
        else:
            field.range = Range(min=options['range']['min'], max=options['range']['max'])

        if not field.range.min <= len(str(answer["answer"])) <= field.range.max:
            errors[answer["position"]] = "Value length is out of range!"
            return False

        return True

    @staticmethod
    def validate_data(form_result):
        """

        :param form_result:
        :return: True or False, errors
        """
        positions_passed, errors = FormResultService._validate_answers_positions(form_result)
        if not positions_passed:
            return positions_passed, errors
        answers_passed, errors = FormResultService._validate_answers(form_result)
        return answers_passed, errors

    @staticmethod
    def create_answers_dict(form_id, answers):
        """
        Create answers to specific form

        :param form_id:
        :param answers:
        :return: answers dictionary
        """
        form_fields = FormFieldService.filter(form_id=form_id)
        result = {}
        for form_field in form_fields:
            for answer in answers:
                if answer['position'] == form_field.position:
                    result[form_field.question] = answer['answer']
                    break
        return result

    @staticmethod
    def validate_schema(data):
        """
        Validate data for FormResultSchema
        """
        schema = FormResultPostSchema()
        errors = schema.validate(data)
        return (not bool(errors), errors)
