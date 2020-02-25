"""empty message

Revision ID: 62a4241036de
Revises: 04fa8b9610f0
Create Date: 2020-02-25 17:20:18.480983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62a4241036de'
down_revision = '04fa8b9610f0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('form_results', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.create_unique_constraint('unique_user_form', 'form_results', ['user_id', 'form_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_user_form', 'form_results', type_='unique')
    op.alter_column('form_results', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
