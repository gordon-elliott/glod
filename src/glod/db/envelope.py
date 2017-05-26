__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.db import RelationMap, TableMap, PagedQuery, InstanceQuery

from glod.model.envelope import Envelope
from glod.model.envelope_collection import EnvelopeCollection
from glod.model.references import envelope__counterparty, envelope__parishioner

from glod.db.db_column_type_map import DB_COLUMN_TYPE_MAP


TableMap(
    Envelope,
    'envelope',
    DB_COLUMN_TYPE_MAP,
    RelationMap(
        envelope__counterparty,
        'counterparty._id',
        backref='envelopes',
        lazy='joined'
    ),
    RelationMap(
        envelope__parishioner,
        'parishioner._id',
        backref='envelopes',
        lazy='joined'
    ),
)


class EnvelopeInstanceQuery(InstanceQuery):
    def __init__(self, session):
        super().__init__(Envelope, EnvelopeCollection, session)


class EnvelopeQuery(PagedQuery):
    def __init__(self, session):
        super().__init__(Envelope, EnvelopeCollection, session)
