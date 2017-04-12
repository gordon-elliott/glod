__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from graphene.relay import Node

from glod.api.fund_leaf import FundLeaf, fund_fields
from glod.db.fund import FundQuery


class FundNode(FundLeaf):
    class Meta:
        interfaces = (Node,)
        local_fields = fund_fields


def resolve_funds(self, args, context, info):
    session = context['request']['session']
    funds = list(FundQuery(session).collection())
    return funds
