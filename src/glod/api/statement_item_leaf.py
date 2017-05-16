__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene
from graphene.relay import Node

from a_tuin.api import get_local_fields, with_session, OBJECT_REFERENCE_MAP
from glod.db.statement_item import StatementItem, StatementItemInstanceQuery

statement_item_fields = get_local_fields(StatementItem)


class StatementItemLeaf(graphene.ObjectType):
    class Meta:
        interfaces = (Node,)
        local_fields = statement_item_fields

    @classmethod
    @with_session
    def get_node(cls, id_, context, info, session):
        return StatementItemInstanceQuery(session).instance(id_)


OBJECT_REFERENCE_MAP['statement_item'] = StatementItemLeaf
