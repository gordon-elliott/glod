__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.db import TableMap, PagedQuery, InstanceQuery

from glod.model.parish_list.parishioner import Parishioner, ParishionerCollection

from glod.db.db_column_type_map import DB_COLUMN_TYPE_MAP
from glod.db.constants import SCHEMA_NAME


TableMap(Parishioner, SCHEMA_NAME, 'parishioner', DB_COLUMN_TYPE_MAP)
# TODO enforce unique constraint on refernece no


class ParishionerInstanceQuery(InstanceQuery):
    def __init__(self, session):
        super().__init__(Parishioner, ParishionerCollection, session)


class ParishionerQuery(PagedQuery):
    def __init__(self, session):
        super().__init__(Parishioner, ParishionerCollection, session)
