__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.db import TableMap, Query

from glod.model.nominal_account  import (
    NominalAccount,
    NominalAccountSOFAHeading,
    NominalAccountCategory,
    NominalAccountSubCategory,
)
from glod.model.nominal_account_collection import NominalAccountCollection

from glod.db.db_column_type_map import DB_COLUMN_TYPE_MAP


TableMap(NominalAccount, 'nominal_account', DB_COLUMN_TYPE_MAP)


class NominalAccountQuery(Query):
    def __init__(self, session):
        super().__init__(NominalAccount, NominalAccountCollection, session)