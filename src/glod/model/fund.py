__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from enum import IntEnum

from a_tuin.metadata import (
    ObjectReferenceField, IntEnumField, StringField, BooleanField, ArgsFieldGroup, ObjectFieldGroupMeta
)


class FundType(IntEnum):
    Unrestricted = 1
    Restricted = 2
    Endowment = 3


class FundTypeField(IntEnumField):
    def __init__(self, name, required=False, default=None, description=None, validation=None):
        super().__init__(name, FundType, required, default, description, validation)


class Fund(object, metaclass=ObjectFieldGroupMeta):

    constructor_parameters = ArgsFieldGroup(
        (
            StringField('name'),
            FundTypeField('type'),
            BooleanField('is_parish_fund'),
            ObjectReferenceField('account'),
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
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def is_parish_fund(self):
        return self._is_parish_fund

    @is_parish_fund.setter
    def is_parish_fund(self, value):
        self._is_parish_fund = value

    @property
    def account(self):
        return self._account

    @account.setter
    def account(self, value):
        self._account = value
