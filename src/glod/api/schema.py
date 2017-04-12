__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene

from graphene.relay import Node, ConnectionField

from glod.api.account_node import AccountNode, resolve_accounts
from glod.api.fund_node import FundNode, resolve_funds


class RootQueryType(graphene.ObjectType):
    node = Node.Field()
    accounts = ConnectionField(
        AccountNode,
        resolver=resolve_accounts,
        description='List of all accounts'
    )
    funds = ConnectionField(
        FundNode,
        resolver=resolve_funds,
        description='List of all funds'
    )


schema = graphene.Schema(query=RootQueryType)
