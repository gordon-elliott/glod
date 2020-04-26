__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.db import TableMap, PagedQuery, InstanceQuery

from glod.model.address import Address, AddressCollection

from glod.db.db_column_type_map import DB_COLUMN_TYPE_MAP
from glod.db.constants import SCHEMA_NAME


TableMap(Address, SCHEMA_NAME, 'address', DB_COLUMN_TYPE_MAP)


class AddressInstanceQuery(InstanceQuery):
    def __init__(self, session):
        super().__init__(Address, AddressCollection, session)


class AddressQuery(PagedQuery):
    def __init__(self, session):
        super().__init__(Address, AddressCollection, session)
