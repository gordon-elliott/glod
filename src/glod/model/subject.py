__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

from a_tuin.metadata import StringField, ArgsFieldGroup, ObjectFieldGroupMeta


class Subject(object, metaclass=ObjectFieldGroupMeta):

    constructor_parameters = ArgsFieldGroup(
        (
            StringField('name'),
            StringField('select_vestry_summary'),
            StringField('easter_vestry_summary'),
        )
    )

    # metaclass takes care of dealing with the args
    def __init__(self, *args, **kwargs):
        pass

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def select_vestry_summary(self):
        return self._select_vestry_summary

    @select_vestry_summary.setter
    def select_vestry_summary(self, value):
        self._select_vestry_summary = value

    @property
    def easter_vestry_summary(self):
        return self._easter_vestry_summary

    @easter_vestry_summary.setter
    def easter_vestry_summary(self, value):
        self._easter_vestry_summary = value
