"""
SharedForm schemas
"""

from marshmallow import fields

from app import MA


class SharedFormPostSchema(MA.Schema):
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
    # nbf = fields.DateTime(format="%Y-%m-%dT%H:%M:%S.f", required=False)
    nbf = fields.DateTime(required=False)
    exp = fields.DateTime(required=False)


class SharedFormGetSchema(MA.Schema):
    """
    SharedForm schema to use on GET request
    """
    class Meta:
        """
        Fields of SharedForm schema to use on GET request
        """
        fields = ("nbf", "exp")

    nbf = fields.DateTime(required=False)
    exp = fields.DateTime(required=False)





# {
#   "groups_ids": [
#     1, 2
#   ],
#   "users_emails": [
#     "yurdosii.ksv@gmail.com"
#   ],
#   "nbf": "2020-03-31T09:38:47.246Z",
#   "exp": "2020-03-31T09:39:47.246Z"
# }