__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.api import (
    node_class,
    node_connection_field,
    get_update_mutation,
    get_create_mutation
)
from glod.api.parishioner_leaf import ParishionerLeaf, parishioner_fields
from glod.db.parishioner import Parishioner, ParishionerQuery


ParishionerNode = node_class(Parishioner.__name__, ParishionerLeaf, parishioner_fields)

parishioners_connection_field = node_connection_field(
    ParishionerQuery,
    ParishionerNode,
    description="List of all parishioners"
)
CreateParishionerLeaf = get_create_mutation(Parishioner, parishioner_fields, ParishionerLeaf)
UpdateParishionerLeaf = get_update_mutation(Parishioner, parishioner_fields, ParishionerLeaf)
