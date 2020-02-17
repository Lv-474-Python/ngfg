"""empty message

Revision ID: a4ff0ba9384a
Revises: 
Create Date: 2020-02-17 18:22:21.183812

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4ff0ba9384a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('answers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('value')
    )
    op.create_table('ranges',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('min', sa.Integer(), nullable=True),
    sa.Column('max', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('google_token', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('google_token'),
    sa.UniqueConstraint('username')
    )
    op.create_table('fields',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('field_type', sa.SmallInteger(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', 'owner_id', name='unique_name_owner')
    )
    op.create_table('forms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('result_url', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('owner_id', 'name', name='owner_form_name')
    )
    op.create_table('choice_options',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('field_id', sa.Integer(), nullable=True),
    sa.Column('option_text', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['field_id'], ['fields.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('field_id', 'option_text', name='unique_field_option_text')
    )
    op.create_table('fields_range',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('field_id', sa.Integer(), nullable=False),
    sa.Column('range_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['field_id'], ['fields.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['range_id'], ['ranges.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('field_id')
    )
    op.create_table('form_fields',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('form_id', sa.Integer(), nullable=False),
    sa.Column('field_id', sa.Integer(), nullable=False),
    sa.Column('question', sa.Text(), nullable=False),
    sa.Column('position', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['field_id'], ['fields.id'], ),
    sa.ForeignKeyConstraint(['form_id'], ['forms.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('form_id', 'position', name='unique_form_position')
    )
    op.create_table('form_results',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('answer', sa.JSON(), nullable=False),
    sa.Column('form_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['form_id'], ['forms.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('settings_autocomplete',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data_url', sa.Text(), nullable=False),
    sa.Column('sheet', sa.Text(), nullable=False),
    sa.Column('from_row', sa.String(), nullable=True),
    sa.Column('to_row', sa.String(), nullable=True),
    sa.Column('field_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['field_id'], ['fields.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('settings_strict',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_strict', sa.Boolean(), nullable=True),
    sa.Column('field_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['field_id'], ['fields.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('field_id', name='unique_field')
    )
    op.create_table('shared_fields',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('field_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['field_id'], ['fields.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'field_id', name='unique_user_field')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shared_fields')
    op.drop_table('settings_strict')
    op.drop_table('settings_autocomplete')
    op.drop_table('form_results')
    op.drop_table('form_fields')
    op.drop_table('fields_range')
    op.drop_table('choice_options')
    op.drop_table('forms')
    op.drop_table('fields')
    op.drop_table('users')
    op.drop_table('ranges')
    op.drop_table('answers')
    # ### end Alembic commands ###
