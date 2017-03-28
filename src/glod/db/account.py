__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.db import TableMap, Query

from glod.model.account import Account, AccountStatus
from glod.model.account_collection import AccountCollection

from glod.db.db_column_type_map import DB_COLUMN_TYPE_MAP


TableMap(Account, 'account', DB_COLUMN_TYPE_MAP)


class AccountQuery(Query):
    def __init__(self, session):
        super().__init__(Account, AccountCollection, session)