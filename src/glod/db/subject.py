__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.db import TableMap, Query

from glod.model.subject import Subject
from glod.model.subject_collection import SubjectCollection

from glod.db.db_column_type_map import DB_COLUMN_TYPE_MAP


TableMap(Subject, 'subject', DB_COLUMN_TYPE_MAP)


class SubjectQuery(Query):
    def __init__(self, session):
        super().__init__(Subject, SubjectCollection, session)
