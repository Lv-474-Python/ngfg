"""
FormResult model
"""
from marshmallow import fields, ValidationError
from sqlalchemy import func

from app import DB, MA
from .abstract_model import AbstractModel


class FormResult(AbstractModel):
    """
    FormResult model class
    :param user_id: user who answered to field
    :param answer: json {position: answer_id}
    :param form_id: id to table Form
    """
    __tablename__ = 'form_results'
    __table_args__ = (
        DB.UniqueConstraint('user_id', 'form_id', name='unique_user_form'),
    )

    user_id = DB.Column(DB.Integer, DB.ForeignKey('users.id'),
                        nullable=True)
    answers = DB.Column(DB.JSON, nullable=False)
    form_id = DB.Column(DB.Integer, DB.ForeignKey('forms.id'),
                        nullable=False)
    created = DB.Column(DB.TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return (f"<FormResult {self.id}, user: {self.user}, "
                f"answers: {self.answers}, form_id: {self.form.id}")


class Keys(fields.Field):
    """
    Custom field to check answers dict keys
    """

    def _deserialize(self, value, attr, data, **kwargs):
        """
        Deserialization method

        :param value:
        :param attr:
        :param data:
        :param kwargs:
        :return:
        """
        if value not in ("position", "answer"):
            raise ValidationError("Wrong answer key")
        return value


class FormResultSchema(MA.Schema):  # pylint: disable=too-many-ancestors
    """
    FormResult marshmallow schema
    """
    class Meta:
        """
        Schema meta
        """
        fields = ("id", "user_id", "form_id", "created", "answers")

    user_id = fields.Int(required=True)
    form_id = fields.Int(required=True)
    result_url = fields.Url(required=True)
    answers = fields.List(fields.Dict(keys=Keys, values=fields.Raw()))
