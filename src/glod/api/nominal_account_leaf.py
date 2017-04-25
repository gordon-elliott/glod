__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene
from graphene.relay import Node

from a_tuin.api import get_local_fields, with_session, OBJECT_REFERENCE_MAP
from glod.db.nominal_account import NominalAccount, NominalAccountQuery

nominal_account_fields = get_local_fields(NominalAccount)


class NominalAccountLeaf(graphene.ObjectType):
    class Meta:
        interfaces = (Node,)
        local_fields = nominal_account_fields

    @classmethod
    @with_session
    def get_node(cls, id_, context, info, session):
        return NominalAccountQuery(session).instance(id_)


OBJECT_REFERENCE_MAP['nominal_account'] = NominalAccountLeaf
