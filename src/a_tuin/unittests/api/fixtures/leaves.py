__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene

from a_tuin.api.types import OBJECT_REFERENCE_MAP
from a_tuin.api.leaf import leaf_class_interfaces

from a_tuin.unittests.api.fixtures.models import (
    AClass,
    AReferringClass,
)
from a_tuin.unittests.api.fixtures.mapping import (
    with_session,
    AClassQuery,
    AReferringClassQuery,
)


class AClassLeaf(graphene.ObjectType):

    class Meta:
        interfaces = leaf_class_interfaces(AClass)

    @classmethod
    @with_session
    def get_node(cls, id_, context, info, session):
        return AClassQuery(session).instance(id_)

OBJECT_REFERENCE_MAP['aclass'] = AClassLeaf


class AReferringClassLeaf(graphene.ObjectType):
    class Meta:
        interfaces = leaf_class_interfaces(AReferringClass)

    @classmethod
    @with_session
    def get_node(cls, id_, context, info, session):
        return AReferringClassQuery(session).instance(id_)


OBJECT_REFERENCE_MAP['areferringclass'] = AReferringClassLeaf
