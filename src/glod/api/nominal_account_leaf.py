__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene

from a_tuin.api import id_with_session, OBJECT_REFERENCE_MAP, leaf_class_interfaces
from glod.db.nominal_account import NominalAccount, NominalAccountInstanceQuery


class NominalAccountLeaf(graphene.ObjectType):
    class Meta:
        interfaces = leaf_class_interfaces(NominalAccount)

    @classmethod
    @id_with_session
    def get_node(cls, id_, context, info, session):
        return NominalAccountInstanceQuery(session).instance(id_)


OBJECT_REFERENCE_MAP['nominal_account'] = NominalAccountLeaf
