__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from enum import IntEnum

from a_tuin.metadata import (
    ObjectReferenceField, IntEnumField, StringField, BooleanField, ObjectFieldGroupBase
)


class FundType(IntEnum):
    Unrestricted = 1
    Restricted = 2
    Endowment = 3


class FundTypeField(IntEnumField):
    def __init__(self, name, is_mutable=True, required=False, default=None, description=None, validation=None):
        super().__init__(name, FundType, is_mutable, required, default, description, validation)


class Fund(ObjectFieldGroupBase):

    public_interface = (
        (
            StringField('name'),
            FundTypeField('type'),
            BooleanField('is_parish_fund'),
            ObjectReferenceField('account'),
        )
    )
