__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

from a_tuin.metadata import StringField, ObjectFieldGroupBase, Collection


class Subject(ObjectFieldGroupBase):

    public_interface = (
        StringField('name'),
        StringField('select_vestry_summary'),
        StringField('easter_vestry_summary'),
    )


class SubjectCollection(Collection):
    pass
