__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene

from a_tuin.api import id_with_session, OBJECT_REFERENCE_MAP, leaf_class_interfaces
from glod.db.statement_item import StatementItem, StatementItemInstanceQuery


class StatementItemLeaf(graphene.ObjectType):
    class Meta:
        interfaces = leaf_class_interfaces(StatementItem)

    @classmethod
    @id_with_session
    def get_node(cls, id_, context, info, session):
        return StatementItemInstanceQuery(session).instance(id_)


OBJECT_REFERENCE_MAP['statement_item'] = StatementItemLeaf
