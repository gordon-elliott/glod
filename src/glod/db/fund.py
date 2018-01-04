__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.db import TableMap, RelationMap, PagedQuery, InstanceQuery

from glod.model.fund import Fund, FundRestriction, FundCollection
from glod.model.references import fund__account

from glod.db.db_column_type_map import DB_COLUMN_TYPE_MAP

TableMap(
    Fund,
    'fund',
    DB_COLUMN_TYPE_MAP,
    RelationMap(
        fund__account,
        'account._id',
        backref='funds',
        lazy='joined'
    ),
)

class FundInstanceQuery(InstanceQuery):
    def __init__(self, session):
        super().__init__(Fund, FundCollection, session)


class FundQuery(PagedQuery):
    def __init__(self, session):
        super().__init__(Fund, FundCollection, session)
