__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.db import RelationMap, TableMap

from glod.model.statement_item import StatementItem
from glod.model.references import statement_item__account

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
