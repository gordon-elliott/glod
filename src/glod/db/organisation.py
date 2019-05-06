__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.db import TableMap, PagedQuery, InstanceQuery

from glod.model.organisation import Organisation, OrganisationCollection, OrganisationCategory, OrganisationStatus

from glod.db.db_column_type_map import DB_COLUMN_TYPE_MAP
from glod.db.constants import SCHEMA_NAME


TableMap(Organisation, SCHEMA_NAME, 'organisation', DB_COLUMN_TYPE_MAP)


class OrganisationInstanceQuery(InstanceQuery):
    def __init__(self, session):
        super().__init__(Organisation, OrganisationCollection, session)


class OrganisationQuery(PagedQuery):
    def __init__(self, session):
        super().__init__(Organisation, OrganisationCollection, session)
