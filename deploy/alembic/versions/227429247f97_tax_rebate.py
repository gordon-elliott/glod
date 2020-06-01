__copyright__ = 'Copyright(c) Gordon Elliott 2019'

""" Store PPS numbers and tracking information for them

Revision ID: 227429247f97
Revises: 6fb351569d30
Create Date: 2020-05-31 16:30:45.964280

"""
from alembic import op
import sqlalchemy as sa

from glod.model.pps import PPSStatus


# revision identifiers, used by Alembic.
revision = '227429247f97'
down_revision = '6fb351569d30'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tax_rebate',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=64), nullable=False),
        sa.Column('2015_rebate', sa.String(length=64), nullable=True),
        sa.Column('2016_rebate', sa.String(length=64), nullable=True),
        sa.Column('2017_rebate', sa.String(length=64), nullable=True),
        sa.Column('2018_rebate', sa.String(length=64), nullable=True),
        sa.Column('person_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['person_id'], ['glod.person.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='glod'
    )

    status_strings = [s.name for s in PPSStatus]
    status_enum = sa.Enum(*status_strings, name='ppsstatus', schema='glod', inherit_schema=True)
    status_enum.create(op.get_bind(), checkfirst=False)
    op.add_column(
        'pps',
        sa.Column('status', status_enum, default=PPSStatus.Requested, nullable=True),
        schema='glod'
    )
    op.add_column(
        'pps',
        sa.Column('chy3_valid_year', sa.Integer(), nullable=True),
        schema='glod'
    )


def downgrade():
    op.drop_table('tax_rebate', schema='glod')

    op.drop_column('pps', 'status', schema='glod')
    op.drop_column('pps', 'chy3_valid_year', schema='glod')
