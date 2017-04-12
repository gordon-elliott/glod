__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene

from graphene.relay import Node

from glod.api.types import OBJECT_REFERENCE_MAP
from glod.api.graphene import get_local_fields
from glod.db.fund import Fund, FundQuery


fund_fields = get_local_fields(Fund)


class FundLeaf(graphene.ObjectType):
    class Meta:
        interfaces = (Node,)
        local_fields = fund_fields

    @classmethod
    def get_node(cls, id_, context, info):
        session = context['request']['session']
        return FundQuery(session).instance(id_)


OBJECT_REFERENCE_MAP['fund'] = FundLeaf
