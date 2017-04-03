__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

from enum import IntEnum

from a_tuin.metadata import IntField, IntEnumField, StringField, ArgsFieldGroup, ObjectFieldGroupMeta


class AccountStatus(IntEnum):
    Active = 1
    Closed = 2


class AccountStatusField(IntEnumField):
    def __init__(self, name, required=False, default=None, description=None, validation=None):
        super().__init__(name, AccountStatus, required, default, description, validation)


class Account(object, metaclass=ObjectFieldGroupMeta):

    constructor_parameters = ArgsFieldGroup(
        (
            IntField('reference_no'),
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

    # metaclass takes care of dealing with the args
    def __init__(self, *args, **kwargs):
        pass

    @property
    def id(self):
        return self._id

    @property
    def reference_no(self):
        return self._reference_no

    @property
    def purpose(self):
        return self._purpose

    @purpose.setter
    def purpose(self, value):
        self._purpose = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def institution(self):
        return self._institution

    @institution.setter
    def institution(self, value):
        self._institution = value

    @property
    def sort_code(self):
        return self._sort_code

    @sort_code.setter
    def sort_code(self, value):
        self._sort_code = value

    @property
    def account_no(self):
        return self._account_no

    @account_no.setter
    def account_no(self, value):
        self._account_no = value

    @property
    def BIC(self):
        return self._BIC

    @BIC.setter
    def BIC(self, value):
        self._BIC = value

    @property
    def IBAN(self):
        return self._IBAN

    @IBAN.setter
    def IBAN(self, value):
        self._IBAN = value
