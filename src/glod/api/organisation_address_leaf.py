__copyright__ = 'Copyright(c) Gordon Elliott 2018'

""" 
"""

import graphene

from a_tuin.api import id_with_session, OBJECT_REFERENCE_MAP, leaf_class_interfaces
from glod.db.organisation_address import OrganisationAddress, OrganisationAddressInstanceQuery


class OrganisationAddressLeaf(graphene.ObjectType):
    class Meta:
        interfaces = leaf_class_interfaces(OrganisationAddress)

    @classmethod
    @id_with_session
    def get_node(cls, id_, context, info, session):
        return OrganisationAddressInstanceQuery(session).instance(id_)


OBJECT_REFERENCE_MAP['organisation_address'] = OrganisationAddressLeaf
