"""
Form database model.
Table for storing descriptive information about the form.
"""
from sqlalchemy import func

from app import DB
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
    created = DB.Column(DB.TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    fields = DB.relationship('FormField', backref='form', cascade='all,delete')
    form_results = DB.relationship('FormResult', backref='form')
