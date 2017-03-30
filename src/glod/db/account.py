__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.db import TableMap, Query

from glod.model.account import Account
from glod.model.account_collection import AccountCollection


TableMap(Account, 'account')


class AccountQuery(Query):
    def __init__(self, session):
        super().__init__(Account, AccountCollection, session)