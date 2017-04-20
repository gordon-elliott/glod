__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from glod.api.graphene import node_connection_field, get_update_mutation, get_create_mutation

from glod.db.subject import Subject, SubjectQuery
from glod.api.subject_leaf import SubjectLeaf, subject_fields


subjects_connection_field = node_connection_field(
    SubjectQuery,
    SubjectLeaf,
    subject_fields,
    description="List of all subjects"
)
CreateSubjectLeaf = get_create_mutation(Subject, subject_fields, SubjectLeaf)
UpdateSubjectLeaf = get_update_mutation(Subject, subject_fields, SubjectLeaf)
