__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from graphene.relay import Node

from glod.db.subject import SubjectQuery
from glod.api.subject_leaf import SubjectLeaf, subject_fields


class SubjectNode(SubjectLeaf):
    class Meta:
        interfaces = (Node,)
        local_fields = subject_fields


def resolve_subjects(self, args, context, info):
    session = context['request']['session']
    subjects = list(SubjectQuery(session).collection())
    return subjects


