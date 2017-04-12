__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from graphene.relay import Node

from glod.db.nominal_account import NominalAccountQuery
from glod.api.nominal_account_leaf import NominalAccountLeaf, nominal_account_fields


class NominalAccountNode(NominalAccountLeaf):
    class Meta:
        interfaces = (Node,)
        local_fields = nominal_account_fields


def resolve_nominal_accounts(self, args, context, info):
    session = context['request']['session']
    nominal_accounts = list(NominalAccountQuery(session).collection())
    return nominal_accounts


