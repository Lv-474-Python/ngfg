"""
SharedForm schemas
"""

from marshmallow import fields, validates_schema, ValidationError

from app import MA


class SharedFormFlagsSchema(MA.Schema):
    """
    SharedFormFlags schema to use on POST, GET requests
    """
    class Meta:
        """
        Fields of SharedFormFlags schema
        """
        fields = ("nbf", "exp")

    nbf = fields.DateTime(required=False)
    exp = fields.DateTime(required=False)

    @validates_schema
    # pylint:disable=no-self-use
    def validate_flags(self, data, **kwargs):
        """
        Validates flags

        :param data: data to validate
        """
        nbf, exp = data.get('nbf'), data.get('exp')
        if nbf is not None and exp is not None and nbf >= exp:
            raise ValidationError({'_schema': "nbf has to be before exp"})


class SharedFormPostSchema(SharedFormFlagsSchema):
    """
    SharedForm schema to use on POST request
    """
    class Meta:
        """
        Fields of SharedForm schema to use on POST request
        """
        fields = ("groups_ids", "users_emails", "nbf", "exp")

    groups_ids = fields.List(fields.Integer(), required=True)
    users_emails = fields.List(fields.Email(), required=True)
