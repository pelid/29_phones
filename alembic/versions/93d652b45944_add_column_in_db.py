"""add column in db

Revision ID: 93d652b45944
Revises:
Create Date: 2017-08-26 16:19:28.174395

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93d652b45944'
down_revision = None
branch_labels = None
depends_on = None
string_len = 10

def upgrade():
    op.add_column('orders', sa.Column('normalized_phone_number', sa.String(string_len)))


def downgrade():
    op.drop_column('orders', 'normalized_phone_number')
