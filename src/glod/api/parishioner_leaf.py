__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene
from graphene.relay import Node

from a_tuin.api import get_local_fields, with_session, OBJECT_REFERENCE_MAP
from glod.db.parishioner import Parishioner, ParishionerInstanceQuery

parishioner_fields = get_local_fields(Parishioner)


class ParishionerLeaf(graphene.ObjectType, interfaces=(Node,)):
    class Meta:
        local_fields = parishioner_fields

    @classmethod
    @with_session
    def get_node(cls, id_, context, info, session):
        return ParishionerInstanceQuery(session).instance(id_)


OBJECT_REFERENCE_MAP['parishioner'] = ParishionerLeaf
