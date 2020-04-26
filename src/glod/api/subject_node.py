__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.api import (
    node_class,
    node_connection_field,
    get_update_mutation,
    get_create_mutation,
    get_local_fields
)
from glod.api.subject_leaf import SubjectLeaf
from glod.db.subject import Subject, SubjectQuery


subject_fields = get_local_fields(Subject)

SubjectNode = node_class(Subject.__name__, SubjectLeaf, subject_fields)

subjects_connection_field = node_connection_field(
    Subject,
    SubjectQuery,
    SubjectNode,
    description="List of all subjects"
)

subjects_options_field = node_connection_field(
    Subject,
    SubjectQuery,
    SubjectLeaf,
    description="List of all subjects for Select fields"
)

CreateSubjectLeaf = get_create_mutation(Subject, subject_fields, SubjectLeaf)
UpdateSubjectLeaf = get_update_mutation(Subject, subject_fields, SubjectLeaf)
