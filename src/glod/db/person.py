__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.db import TableMap, RelationMap, PagedQuery, InstanceQuery

from glod.model.person import Person, PersonCollection
from glod.model.references import person__organisation

from glod.db.db_column_type_map import DB_COLUMN_TYPE_MAP


TableMap(
    Person,
    'person',
    DB_COLUMN_TYPE_MAP,
    RelationMap(
        person__organisation,
        'organisation._id',
        backref='people',
        lazy='joined'
    ),
)


class PersonInstanceQuery(InstanceQuery):
    def __init__(self, session):
        super().__init__(Person, PersonCollection, session)


class PersonQuery(PagedQuery):
    def __init__(self, session):
        super().__init__(Person, PersonCollection, session)
