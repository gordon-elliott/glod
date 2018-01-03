__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.db import TableMap, RelationMap, PagedQuery, InstanceQuery

from glod.model.organisation_address import OrganisationAddress, OrganisationAddressCollection
from glod.model.references import organisation_address__address, organisation_address__organisation

from glod.db.db_column_type_map import DB_COLUMN_TYPE_MAP

# TODO upgrade to SQLA 1.2 when it's available and use lazy=selectin

TableMap(
    OrganisationAddress,
    'organisation_address',
    DB_COLUMN_TYPE_MAP,
    RelationMap(
        organisation_address__address,
        'address._id',
        backref='organisation_addresses',
        lazy='select'
    ),
    RelationMap(
        organisation_address__organisation,
        'organisation._id',
        backref='organisation_addresses',
        lazy='joined'
    ),
)


class OrganisationAddressInstanceQuery(InstanceQuery):
    def __init__(self, session):
        super().__init__(OrganisationAddress, OrganisationAddressCollection, session)


class OrganisationAddressQuery(PagedQuery):
    def __init__(self, session):
        super().__init__(OrganisationAddress, OrganisationAddressCollection, session)
