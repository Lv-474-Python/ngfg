"""
Form database model.
Table for storing descriptive information about the form.
"""
from marshmallow import fields

from app import DB, MA
from .abstract_model import AbstractModel


class Form(AbstractModel):
    """
    :param owner_id - int | User who created the form
    :param name - nvarchar | Name, for the owner to search his forms
    :param title -  nvarchar | Form title visible for all users
    :param result_url - text | Url for the domain where form results are stored
     (e.g. Url to Google Sheets)
    :param is_published - bool | True - Form is published and can`t be changed
    """

    __tablename__ = 'forms'
    __table_args__ = (DB.UniqueConstraint('owner_id', 'name',
                                          name='owner_form_name'),
                      )

    owner_id = DB.Column(DB.Integer, DB.ForeignKey('users.id'),
                         nullable=False)
    name = DB.Column(DB.String, nullable=False)
    title = DB.Column(DB.String, nullable=False)
    result_url = DB.Column(DB.Text)
    is_published = DB.Column(DB.Boolean, nullable=False)

    fields = DB.relationship('FormField', backref='form', cascade='all,delete')
    form_results = DB.relationship('FormResult', backref='form')


class FormSchema(MA.Schema):
    """
    Form schema

    :param name - str
    :param title - str
    :param result_url - url
    :param is_published - bool
    """
    class Meta:
        """
        Form schema meta
        """
        fields = ("id", "owner_id", "name", "title", "result_url", "is_published")

    owner_id = fields.Int(dump_only=True, data_key='ownerId')
    name = fields.Str(required=True)
    title = fields.Str(required=True)
    result_url = fields.Url(required=True, data_key='resultUrl')
    is_published = fields.Bool(required=True, data_key='isPublished')
