__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene

from graphene.relay import Node

from glod.api.types import OBJECT_REFERENCE_MAP
from glod.api.graphene import get_local_fields, with_session
from glod.db.subject import Subject, SubjectQuery


subject_fields = get_local_fields(Subject)


class SubjectLeaf(graphene.ObjectType):
    class Meta:
        interfaces = (Node,)
        local_fields = subject_fields

    @classmethod
    @with_session
    def get_node(cls, id_, context, info, session):
        return SubjectQuery(session).instance(id_)


OBJECT_REFERENCE_MAP['subject'] = SubjectLeaf
