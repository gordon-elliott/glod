__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.db import RelationMap, TableMap, PagedQuery, InstanceQuery

from glod.model.counterparty import Counterparty, CounterpartyCollection
from glod.model.references import counterparty__person, counterparty__organisation

from glod.db.db_column_type_map import DB_COLUMN_TYPE_MAP
from glod.db.constants import SCHEMA_NAME


TableMap(Counterparty, SCHEMA_NAME, 'counterparty', DB_COLUMN_TYPE_MAP, RelationMap(
    counterparty__person,
    'person._id',
    backref='counterparties',
    lazy='selectin'
), RelationMap(
    counterparty__organisation,
    'organisation._id',
    backref='counterparties',
    lazy='selectin'
))


class CounterpartyInstanceQuery(InstanceQuery):
    def __init__(self, session):
        super().__init__(Counterparty, CounterpartyCollection, session)


class CounterpartyQuery(PagedQuery):
    def __init__(self, session):
        super().__init__(Counterparty, CounterpartyCollection, session)
