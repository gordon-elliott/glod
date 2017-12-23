__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene
from graphene.relay import Node

from a_tuin.api import get_local_fields, with_session, OBJECT_REFERENCE_MAP
from glod.db.account import Account, AccountInstanceQuery

account_fields = get_local_fields(Account)


class AccountLeaf(graphene.ObjectType, interfaces=(Node,)):
    class Meta:
        local_fields = account_fields

    @classmethod
    @with_session
    def get_node(cls, id_, context, info, session):
        return AccountInstanceQuery(session).instance(id_)


OBJECT_REFERENCE_MAP['account'] = AccountLeaf
