__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.api import (
    node_class,
    node_connection_field,
    get_update_mutation,
    get_create_mutation,
    get_local_fields
)
from glod.api.parishioner_leaf import ParishionerLeaf
from glod.db.parish_list.parishioner import Parishioner, ParishionerQuery


parishioner_fields = get_local_fields(Parishioner)

ParishionerNode = node_class(Parishioner.__name__, ParishionerLeaf, parishioner_fields)

parishioners_connection_field = node_connection_field(
    Parishioner,
    ParishionerQuery,
    ParishionerNode,
    description="List of all parishioners"
)

parishioners_options_field = node_connection_field(
    Parishioner,
    ParishionerQuery,
    ParishionerLeaf,
    description="List of all parishioners for select fields"
)

CreateParishionerLeaf = get_create_mutation(Parishioner, parishioner_fields, ParishionerLeaf)
UpdateParishionerLeaf = get_update_mutation(Parishioner, parishioner_fields, ParishionerLeaf)
