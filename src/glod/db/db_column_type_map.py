__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""


from sqlalchemy import (
    Enum,
)

from a_tuin.db.mapper import DB_COLUMN_TYPE_MAP

from glod.model.account import AccountStatusField, AccountStatus
from glod.model.fund import FundTypeField, FundType

DB_COLUMN_TYPE_MAP[AccountStatusField] = Enum(AccountStatus)
DB_COLUMN_TYPE_MAP[FundTypeField] = Enum(FundType)
