__copyright__ = 'Copyright(c) Gordon Elliott 2018'

""" 
"""

import graphene

from a_tuin.api import id_with_session, OBJECT_REFERENCE_MAP, leaf_class_interfaces
from glod.db.pps import PPS, PPSInstanceQuery


class PPSLeaf(graphene.ObjectType):
    class Meta:
        interfaces = leaf_class_interfaces(PPS)

    @classmethod
    @id_with_session
    def get_node(cls, id_, context, info, session):
        return PPSInstanceQuery(session).instance(id_)


OBJECT_REFERENCE_MAP['pps'] = PPSLeaf
