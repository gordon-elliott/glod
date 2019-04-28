__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.db import TableMap, PagedQuery, InstanceQuery

from glod.model.parish_list.household import Household, HouseholdCollection

from glod.db.db_column_type_map import DB_COLUMN_TYPE_MAP


TableMap(Household, 'household', DB_COLUMN_TYPE_MAP)
# TODO enforce unique constraint on refernece no


class HouseholdInstanceQuery(InstanceQuery):
    def __init__(self, session):
        super().__init__(Household, HouseholdCollection, session)


class HouseholdQuery(PagedQuery):
    def __init__(self, session):
        super().__init__(Household, HouseholdCollection, session)
