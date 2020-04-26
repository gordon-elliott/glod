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
from glod.api.person_leaf import PersonLeaf
from glod.db.person import Person, PersonQuery


person_fields = get_local_fields(Person)

PersonNode = node_class(Person.__name__, PersonLeaf, person_fields)

persons_connection_field = node_connection_field(
    Person,
    PersonQuery,
    PersonNode,
    description="List of all people"
)

persons_options_field = node_connection_field(
    Person,
    PersonQuery,
    PersonLeaf,
    description="List of all people for Select fields"
)

CreatePersonLeaf = get_create_mutation(Person, person_fields, PersonLeaf)
UpdatePersonLeaf = get_update_mutation(Person, person_fields, PersonLeaf)
