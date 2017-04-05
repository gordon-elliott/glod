__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.db import RelationMap, TableMap

from glod.model.subject import Subject
from glod.model.references import subject__nominal_account

from glod.db.db_column_type_map import DB_COLUMN_TYPE_MAP

TableMap(
    Subject,
    'subject',
    DB_COLUMN_TYPE_MAP,
    RelationMap(
        subject__nominal_account,
        'nominal_account._id',
        backref='subjects',
        lazy='joined'
    ),
)
