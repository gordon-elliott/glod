__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene

from a_tuin.api import id_with_session, OBJECT_REFERENCE_MAP, leaf_class_interfaces
from glod.db.fund import Fund, FundInstanceQuery


class FundLeaf(graphene.ObjectType):
    class Meta:
        interfaces = leaf_class_interfaces(Fund)

    @classmethod
    @id_with_session
    def get_node(cls, id_, context, info, session):
        return FundInstanceQuery(session).instance(id_)


OBJECT_REFERENCE_MAP['fund'] = FundLeaf
