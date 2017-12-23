__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene
from graphene.relay import Node

from a_tuin.api import get_local_fields, with_session, OBJECT_REFERENCE_MAP
from glod.db.subject import Subject, SubjectInstanceQuery

subject_fields = get_local_fields(Subject)


class SubjectLeaf(graphene.ObjectType, interfaces=(Node,)):
    class Meta:
        local_fields = subject_fields

    @classmethod
    @with_session
    def get_node(cls, id_, context, info, session):
        return SubjectInstanceQuery(session).instance(id_)


OBJECT_REFERENCE_MAP['subject'] = SubjectLeaf
