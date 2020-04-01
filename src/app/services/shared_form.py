"""
SharedField service
"""

from datetime import datetime


class SharedFormService:
    """
    SharedForm Service class
    """

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

        datetime_instance = datetime.fromisoformat(datetime_string)
        return datetime_instance
