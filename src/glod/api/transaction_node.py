__copyright__ = 'Copyright(c) Gordon Elliott 2018'

""" 
"""

from a_tuin.api import (
    node_class,
    node_connection_field,
    get_update_mutation,
    get_create_mutation,
    get_local_fields
)
from glod.api.transaction_leaf import TransactionLeaf
from glod.db.transaction import Transaction, TransactionQuery


transaction_fields = get_local_fields(Transaction)

TransactionNode = node_class(Transaction.__name__, TransactionLeaf, transaction_fields)

transactions_connection_field = node_connection_field(
    Transaction,
    TransactionQuery,
    TransactionNode,
    description='List of all transactions'
)

transactions_options_field = node_connection_field(
    Transaction,
    TransactionQuery,
    TransactionLeaf,
    description='List of all transactions for Select fields'
)

CreateTransactionLeaf = get_create_mutation(Transaction, transaction_fields, TransactionLeaf)
UpdateTransactionLeaf = get_update_mutation(Transaction, transaction_fields, TransactionLeaf)
