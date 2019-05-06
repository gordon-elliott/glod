__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.db import RelationMap, TableMap, PagedQuery, InstanceQuery

from glod.model.envelope import Envelope, EnvelopeCollection
from glod.model.references import envelope__counterparty, envelope__person

from glod.db.db_column_type_map import DB_COLUMN_TYPE_MAP
from glod.db.constants import SCHEMA_NAME


TableMap(Envelope, SCHEMA_NAME, 'envelope', DB_COLUMN_TYPE_MAP, RelationMap(
    envelope__counterparty,
    'counterparty._id',
    backref='envelopes',
    lazy='joined'
), RelationMap(
    envelope__person,
    'person._id',
    backref='envelopes',
    lazy='joined'
))


class EnvelopeInstanceQuery(InstanceQuery):
    def __init__(self, session):
        super().__init__(Envelope, EnvelopeCollection, session)


class EnvelopeQuery(PagedQuery):
    def __init__(self, session):
        super().__init__(Envelope, EnvelopeCollection, session)
