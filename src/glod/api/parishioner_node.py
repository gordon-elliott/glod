__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from graphene.relay import Node

from glod.db.parishioner import ParishionerQuery
from glod.api.parishioner_leaf import ParishionerLeaf, parishioner_fields


class ParishionerNode(ParishionerLeaf):
    class Meta:
        interfaces = (Node,)
        local_fields = parishioner_fields


def resolve_parishioners(self, args, context, info):
    # TODO implement paging of DB query
    session = context['request']['session']
    parishioners = list(ParishionerQuery(session).collection())
    return parishioners


