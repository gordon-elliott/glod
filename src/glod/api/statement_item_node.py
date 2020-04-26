__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.api import (
    node_class,
    node_connection_field,
    get_update_mutation,
    get_create_mutation,
    get_local_fields
)
from glod.api.statement_item_leaf import StatementItemLeaf
from glod.db.statement_item import StatementItem, StatementItemQuery


statement_item_fields = get_local_fields(StatementItem)

StatementItemNode = node_class(StatementItem.__name__, StatementItemLeaf, statement_item_fields)

statement_items_connection_field = node_connection_field(
    StatementItem,
    StatementItemQuery,
    StatementItemNode,
    description='List of all statement_items'
)

statement_items_options_field = node_connection_field(
    StatementItem,
    StatementItemQuery,
    StatementItemLeaf,
    description='List of all statement_items for Select fields'
)

CreateStatementItemLeaf = get_create_mutation(StatementItem, statement_item_fields, StatementItemLeaf)
UpdateStatementItemLeaf = get_update_mutation(StatementItem, statement_item_fields, StatementItemLeaf)
