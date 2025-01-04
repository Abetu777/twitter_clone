"""Add last_test_date to User model

Revision ID: 240616ed460f
Revises: aa70701dcf04
Create Date: 2025-01-04 09:54:12.221999

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '240616ed460f'
down_revision = 'aa70701dcf04'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_test_date', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('last_test_date')

    # ### end Alembic commands ###