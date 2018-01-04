__copyright__ = 'Copyright(c) Gordon Elliott 2018'

""" 
"""

import graphene

from a_tuin.api import (
    node_class,
    node_connection_field,
    get_update_mutation,
    get_create_mutation,
    get_local_fields
)
from glod.api.organisation_leaf import OrganisationLeaf
from glod.api.person_node import PersonLeaf
from glod.api.organisation_address_node import OrganisationAddressNode
from glod.db.organisation import Organisation, OrganisationQuery


organisation_fields = get_local_fields(Organisation)
organisation_node_fields = organisation_fields.copy()

organisation_node_fields['people'] = graphene.Field(
    graphene.List(PersonLeaf, description='People for this organisation')
)
organisation_node_fields['organisation_addresses'] = graphene.Field(
    graphene.List(OrganisationAddressNode, description='Addresses for this organisation')
)

OrganisationNode = node_class(Organisation.__name__, OrganisationLeaf, organisation_node_fields)

organisations_connection_field = node_connection_field(
    Organisation,
    OrganisationQuery,
    OrganisationNode,
    description="List of all organisations"
)
CreateOrganisationLeaf = get_create_mutation(Organisation, organisation_fields, OrganisationLeaf)
UpdateOrganisationLeaf = get_update_mutation(Organisation, organisation_fields, OrganisationLeaf)
