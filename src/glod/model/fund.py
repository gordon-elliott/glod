__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from enum import IntEnum

from a_tuin.metadata import (
    ObjectReferenceField,
    IntEnumField,
    StringField,
    BooleanField,
    ObjectFieldGroupBase,
    Collection,
)


class FundRestriction(IntEnum):
    Unrestricted = 1
    Restricted = 2
    Endowment = 3


class FundRestrictionField(IntEnumField):
    def __init__(self, name, is_mutable=True, required=False, default=None, description=None, validation=None):
        super().__init__(name, FundRestriction, is_mutable, required, default, description, validation)


class Fund(ObjectFieldGroupBase):

    public_interface = (
        StringField('name'),
        FundRestrictionField('restriction'),
        BooleanField('is_parish_fund'),
        ObjectReferenceField('account'),
    )


class FundCollection(Collection):
    pass
