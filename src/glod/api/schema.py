__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene

from graphene.relay import Node, ConnectionField

from glod.api.account_node import AccountNode, resolve_accounts
from glod.api.fund_node import FundNode, resolve_funds
from glod.api.nominal_account_node import NominalAccountNode, resolve_nominal_accounts
from glod.api.subject_node import SubjectNode, resolve_subjects
from glod.api.parishioner_node import ParishionerNode, resolve_parishioners


class RootQueryType(graphene.ObjectType):
    """ Root query for entity lists which support paging
    """
    node = Node.Field()
    accounts = ConnectionField(
        AccountNode,
        resolver=resolve_accounts,
        description='List of all bank accounts'
    )
    funds = ConnectionField(
        FundNode,
        resolver=resolve_funds,
        description='List of all funds'
    )
    nominal_accounts = ConnectionField(
        NominalAccountNode,
        resolver=resolve_nominal_accounts,
        description='List of all nominal accounts'
    )
    subjects = ConnectionField(
        SubjectNode,
        resolver=resolve_subjects,
        description="List of all subjects"
    )
    parishioners = ConnectionField(
        ParishionerNode,
        resolver=resolve_parishioners,
        description="List of all parishioners"
    )


schema = graphene.Schema(query=RootQueryType)
