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
from glod.api.address_leaf import AddressLeaf
from glod.db.address import Address, AddressQuery


address_fields = get_local_fields(Address)

AddressNode = node_class(Address.__name__, AddressLeaf, address_fields)

addresss_connection_field = node_connection_field(
    Address,
    AddressQuery,
    AddressNode,
    description="List of all addresss"
)
CreateAddressLeaf = get_create_mutation(Address, address_fields, AddressLeaf)
UpdateAddressLeaf = get_update_mutation(Address, address_fields, AddressLeaf)
