__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.db import RelationMap, TableMap, PagedQuery, InstanceQuery

from glod.model.statement_item import StatementItem, StatementItemDesignatedBalance
from glod.model.statement_item_collection import StatementItemCollection
from glod.model.references import statement_item__account

from glod.db.db_column_type_map import DB_COLUMN_TYPE_MAP

TableMap(
    StatementItem,
    'statement_item',
    DB_COLUMN_TYPE_MAP,
    RelationMap(
        statement_item__account,
        'account._id',
        backref='statement_items',
        lazy='joined'
    ),
)

class StatementItemInstanceQuery(InstanceQuery):
    def __init__(self, session):
        super().__init__(StatementItem, StatementItemCollection, session)


class StatementItemQuery(PagedQuery):
    def __init__(self, session):
        super().__init__(StatementItem, StatementItemCollection, session)
