__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene
from graphene import Node

from a_tuin.api.types import OBJECT_REFERENCE_MAP
from a_tuin.api import get_local_fields
from a_tuin.unittests.api.fixtures.models import (
    AClass,
    AReferringClass,
)
from a_tuin.unittests.api.fixtures.mapping import (
    with_session,
    AClassQuery,
    AReferringClassQuery,
)


aclass_fields = get_local_fields(AClass)


class AClassLeaf(graphene.ObjectType):
    class Meta:
        interfaces = (Node,)
        local_fields = aclass_fields

    @classmethod
    @with_session
    def get_node(cls, id_, context, info, session):
        return AClassQuery(session).instance(id_)

OBJECT_REFERENCE_MAP['aclass'] = AClassLeaf


areferringclass_fields = get_local_fields(AReferringClass)


class AReferringClassLeaf(graphene.ObjectType):
    class Meta:
        interfaces = (Node,)
        local_fields = areferringclass_fields

    @classmethod
    @with_session
    def get_node(cls, id_, context, info, session):
        return AReferringClassQuery(session).instance(id_)


OBJECT_REFERENCE_MAP['areferringclass'] = AReferringClassLeaf
