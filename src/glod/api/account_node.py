__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene

from graphene.relay import Node

from glod.db.account import AccountQuery
from glod.api.account_leaf import AccountLeaf, account_fields
from glod.api.fund_node import FundLeaf


account_node_fields = account_fields.copy()
account_node_fields['funds'] = graphene.Field(
    graphene.List(FundLeaf, description='Funds for this account.')
)


class AccountNode(AccountLeaf):
    class Meta:
        interfaces = (Node,)
        local_fields = account_node_fields


def resolve_accounts(self, args, context, info):
    session = context['request']['session']
    accounts = list(AccountQuery(session).collection())
    return accounts


