__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.db import RelationMap, TableMap, PagedQuery, InstanceQuery

from glod.model.pps import PPS, PPSCollection
from glod.model.references import pps__person

from glod.db.db_column_type_map import DB_COLUMN_TYPE_MAP


TableMap(
    PPS,
    'pps',
    DB_COLUMN_TYPE_MAP,
    RelationMap(
        pps__person,
        'person._id',
        backref='pps_nos',
        lazy='joined'
    ),
)


class PPSInstanceQuery(InstanceQuery):
    def __init__(self, session):
        super().__init__(PPS, PPSCollection, session)


class PPSQuery(PagedQuery):
    def __init__(self, session):
        super().__init__(PPS, PPSCollection, session)
