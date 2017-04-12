__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene

from graphene.relay import Node

from glod.api.types import OBJECT_REFERENCE_MAP
from glod.api.graphene import get_local_fields
from glod.db.account import Account, AccountQuery


account_fields = get_local_fields(Account)


class AccountLeaf(graphene.ObjectType):
    class Meta:
        interfaces = (Node,)
        local_fields = account_fields

    @classmethod
    def get_node(cls, id_, context, info):
        session = context['request']['session']
        return AccountQuery(session).instance(id_)


OBJECT_REFERENCE_MAP['account'] = AccountLeaf
