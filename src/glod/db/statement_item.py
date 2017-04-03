__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.db import RelationMap, TableMap

from glod.model.statement_item import StatementItem
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
