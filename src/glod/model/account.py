__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

from enum import IntEnum

from a_tuin.metadata import IntField, IntEnumField, StringField, ObjectFieldGroupBase


class AccountStatus(IntEnum):
    Active = 1
    Closed = 2


class AccountStatusField(IntEnumField):
    def __init__(self, name, is_mutable=True, required=False, default=None, description=None, validation=None):
        super().__init__(name, AccountStatus, is_mutable, required, default, description, validation)


class Account(ObjectFieldGroupBase):

    public_interface = (
        (
            IntField('reference_no', is_mutable=False),
            StringField('purpose'),
            AccountStatusField('status'),
            StringField('name'),
            StringField('institution'),
            StringField('sort_code'),
            StringField('account_no'),
            StringField('BIC'),
            StringField('IBAN'),
        )
    )
