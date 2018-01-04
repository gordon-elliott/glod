__copyright__ = 'Copyright(c) Gordon Elliott 2018'

""" 
"""

from a_tuin.api import (
    node_class,
    node_connection_field,
    get_update_mutation,
    get_create_mutation,
    get_local_fields
)
from glod.api.organisation_address_leaf import OrganisationAddressLeaf
from glod.db.organisation_address import OrganisationAddress, OrganisationAddressQuery


organisation_address_fields = get_local_fields(OrganisationAddress)

OrganisationAddressNode = node_class(OrganisationAddress.__name__, OrganisationAddressLeaf, organisation_address_fields)

organisation_addresss_connection_field = node_connection_field(
    OrganisationAddress,
    OrganisationAddressQuery,
    OrganisationAddressNode,
    description="List of all organisation_addresss"
)
CreateOrganisationAddressLeaf = get_create_mutation(OrganisationAddress, organisation_address_fields, OrganisationAddressLeaf)
UpdateOrganisationAddressLeaf = get_update_mutation(OrganisationAddress, organisation_address_fields, OrganisationAddressLeaf)
