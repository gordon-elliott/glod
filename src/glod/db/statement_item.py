__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from glod.db.relation_map import RelationMap
from glod.db.table_map import TableMap
from glod.model.references import statement_item__account
from glod.model.statement_item import StatementItem

TableMap(
    StatementItem,
    'statement_item',
    RelationMap(
        statement_item__account,
        'account._id',
        backref='statement_items',
        lazy='joined'
    ),
)
