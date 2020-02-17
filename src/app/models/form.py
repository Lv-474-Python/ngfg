"""
Form database model.
Table for storing descriptive information about the form.
"""

from app import DB
from .abstract_model import AbstractModel


class Form(AbstractModel):
    """
    :param owner_id - int | User who created the form
    :param name - nvarchar | Name, for the owner to search his forms
    :param title -  nvarchar | Form title visible for all users
    :param result_url - text | Url for the domain where form results are stored
     (e.g. Url to Google Sheets)
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
    fields = DB.relationship('FormField', backref='form')
