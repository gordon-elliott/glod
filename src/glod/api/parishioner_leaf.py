__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene

from a_tuin.api import id_with_session, OBJECT_REFERENCE_MAP, leaf_class_interfaces
from glod.db.parish_list.parishioner import Parishioner, ParishionerInstanceQuery


class ParishionerLeaf(graphene.ObjectType):
    class Meta:
        interfaces = leaf_class_interfaces(Parishioner)

    @classmethod
    @id_with_session
    def get_node(cls, id_, context, info, session):
        return ParishionerInstanceQuery(session).instance(id_)


OBJECT_REFERENCE_MAP['parishioner'] = ParishionerLeaf
