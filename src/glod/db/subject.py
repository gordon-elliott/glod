__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.db import TableMap, PagedQuery, InstanceQuery

from glod.model.subject import Subject, SubjectCollection

from glod.db.db_column_type_map import DB_COLUMN_TYPE_MAP
from glod.db.constants import SCHEMA_NAME


TableMap(Subject, SCHEMA_NAME, 'subject', DB_COLUMN_TYPE_MAP)


class SubjectInstanceQuery(InstanceQuery):
    def __init__(self, session):
        super().__init__(Subject, SubjectCollection, session)


class SubjectQuery(PagedQuery):
    def __init__(self, session):
        super().__init__(Subject, SubjectCollection, session)
