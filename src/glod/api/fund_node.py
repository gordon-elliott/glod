__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from glod.api.fund_leaf import FundLeaf
from glod.db.fund import FundQuery


class FundNode(FundLeaf):
    pass


def resolve_funds(self, args, context, info):
    session = context['request']['session']
    funds = list(FundQuery(session).collection())
    return funds
