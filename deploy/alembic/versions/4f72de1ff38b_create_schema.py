"""create schema

Revision ID: 4f72de1ff38b
Revises: 0e5581770c32
Create Date: 2019-05-06 17:46:31.976863

"""
from alembic import op

from glod.db.constants import SCHEMA_NAME

# revision identifiers, used by Alembic.
revision = '4f72de1ff38b'
down_revision = '0e5581770c32'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("create schema {}".format(SCHEMA_NAME))


def downgrade():
    op.execute("drop schema {}".format(SCHEMA_NAME))
