"""
SharedField service
"""

from datetime import datetime

from app import DB
from app.models import SharedField
from app.helper.decorators import transaction_decorator
from app.helper.errors import SharedFieldNotExist
from app.schemas import SharedFormPostSchema


class SharedFormService:
    """
    SharedForm Service class
    """

    # @staticmethod
    # def to_json(data, many=False):
    #     """
    #     Get data in json format
    #     """
    #     schema = SharedFieldPostSchema(many=many)
    #     return schema.dump(data)

    # @staticmethod
    # def response_to_json(data, many=False):
    #     """
    #     Get response data in json format
    #     """
    #     schema = SharedFieldResponseSchema(many=many)
    #     return schema.dump(data)

    # @staticmethod
    # def get_by_user_and_field(user_id, field_id):
    #     """
    #     Get SharedField instance by user_id and field_id

    #     :param user_id: id of the user to whom the field was shared to
    #     :param field_id: id of the field that was shared
    #     :return: SharedField instance or None
    #     """
    #     shared_field_instance = SharedField.query.filter_by(
    #         user_id=user_id,
    #         field_id=field_id
    #     ).first()
    #     return shared_field_instance

    @staticmethod
    def validate_data(schema, data):
        """
        Validate data by given schema
        """
        errors = schema().validate(data)
        return (not bool(errors), errors)
    
    @staticmethod
    def convertStringToDateTime(datetime_string):
        """
        Convert datetime_string to datetime instance

        Possible strings
        - 2011-11-04T00:05:23
        - 2011-11-04 00:05:23
        - 2011-11-04 00:05:23.521
        - 2011-11-04T00:05:23.321Z - in this case 'Z' should 
        be removed to enable converting
        """

        # check for 'Z'
        if datetime_string[-1] == 'Z':
            datetime_string = datetime_string[:-1]

        #TODO - remove this
        # exp = datetime.strptime(exp, '%Y-%m-%d %H:%M:%S.%f')

        datetime_instance = datetime.fromisoformat(datetime_string)
        return datetime_instance

