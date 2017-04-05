__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.db import TableMap, Query

from glod.model.parishioner import Parishioner
from glod.model.parishioner_collection import ParishionerCollection

from glod.db.db_column_type_map import DB_COLUMN_TYPE_MAP


TableMap(Parishioner, 'parishioner', DB_COLUMN_TYPE_MAP)


class ParishionerQuery(Query):
    def __init__(self, session):
        super().__init__(Parishioner, ParishionerCollection, session)
