__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.db import RelationMap, TableMap, PagedQuery, InstanceQuery

from glod.model.counterparty import Counterparty, StandingOrderDonor, CounterpartyCollection
from glod.model.references import counterparty__parishioner

from glod.db.db_column_type_map import DB_COLUMN_TYPE_MAP


TableMap(
    Counterparty,
    'counterparty',
    DB_COLUMN_TYPE_MAP,
    RelationMap(
        counterparty__parishioner,
        'parishioner._id',
        backref='counterparties',
        lazy='joined'
    ),
)


class CounterpartyInstanceQuery(InstanceQuery):
    def __init__(self, session):
        super().__init__(Counterparty, CounterpartyCollection, session)


class CounterpartyQuery(PagedQuery):
    def __init__(self, session):
        super().__init__(Counterparty, CounterpartyCollection, session)
