__copyright__ = 'Copyright(c) Gordon Elliott 2020'

""" Tables to keep record of tax rebate submissions

Revision ID: 10b2a0ab0e75
Revises: 227429247f97
Create Date: 2020-06-01 13:30:19.224626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10b2a0ab0e75'
down_revision = '227429247f97'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tax_rebate_submission',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=64), nullable=False),
        sa.Column('FY', sa.Integer(), nullable=False),
        sa.Column('calculated_rebate', sa.Numeric(scale=2), nullable=True),
        sa.Column('filing_date', sa.Date(), nullable=True),
        sa.Column('estimated_rebate', sa.Numeric(scale=2), nullable=True),
        sa.Column('notice_number', sa.String(length=64), nullable=True),
        sa.Column('notes', sa.String(length=1024), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        schema='glod'
    )
    op.create_table(
        'person_rebate_submission',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('person_id', sa.Integer(), nullable=True),
        sa.Column('tax_rebate_submission_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['tax_rebate_submission_id'], ['glod.tax_rebate_submission.id'], ),
        sa.ForeignKeyConstraint(['person_id'], ['glod.person.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='glod'
    )


def downgrade():
    op.drop_table('person_rebate_submission', schema='glod')
    op.drop_table('tax_rebate_submission', schema='glod')
