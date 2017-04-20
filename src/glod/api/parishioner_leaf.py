__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene

from graphene.relay import Node

from glod.api.types import OBJECT_REFERENCE_MAP
from glod.api.graphene import get_local_fields, with_session
from glod.db.parishioner import Parishioner, ParishionerQuery


parishioner_fields = get_local_fields(Parishioner)


class ParishionerLeaf(graphene.ObjectType):
    class Meta:
        interfaces = (Node,)
        local_fields = parishioner_fields

    @classmethod
    @with_session
    def get_node(cls, id_, context, info, session):
        return ParishionerQuery(session).instance(id_)


OBJECT_REFERENCE_MAP['parishioner'] = ParishionerLeaf
