__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.db import TableMap, RelationMap, PagedQuery, InstanceQuery

from glod.model.transaction import Transaction, PaymentMethod, IncomeExpenditure, TransactionCollection
from glod.model.references import transaction__counterparty, transaction__subject, transaction__fund

from glod.db.db_column_type_map import DB_COLUMN_TYPE_MAP

# TODO upgrade to SQLA 1.2 when it's available and use lazy=selectin

TableMap(
    Transaction,
    'transaction',
    DB_COLUMN_TYPE_MAP,
    RelationMap(
        transaction__counterparty,
        'counterparty._id',
        backref='transactions',
        lazy='joined'
    ),
    RelationMap(
        transaction__subject,
        'subject._id',
        backref='transactions',
        lazy='select'
    ),
    RelationMap(
        transaction__fund,
        'fund._id',
        backref='transactions',
        lazy='select'
    ),
)


class TransactionInstanceQuery(InstanceQuery):
    def __init__(self, session):
        super().__init__(Transaction, TransactionCollection, session)


class TransactionQuery(PagedQuery):
    def __init__(self, session):
        super().__init__(Transaction, TransactionCollection, session)
