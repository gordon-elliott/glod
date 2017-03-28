__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from csv import DictReader

from glod.model.account import Account, AccountStatus
from glod.model.account_collection import AccountCollection

from a_tuin.metadata import (
    Mapping,
    DictFieldGroup,
    StringField,
    replace_underscore_with_space
)


ACCOUNT_STATUS_MAP = {
    'in use': AccountStatus.Active,
    'ready': AccountStatus.Active,
    'closed': AccountStatus.Closed,
}


class AccountStatusString(StringField):
    def conform_value(self, value):
        return ACCOUNT_STATUS_MAP.get(value.lower(), AccountStatus.Active)


account_csv_fields = Account.constructor_parameters.derive(
    replace_underscore_with_space,
    DictFieldGroup
)
account_csv_fields['reference no'].name = 'id'
account_csv_fields['status'] = AccountStatusString('status')

csv_to_constructor = Mapping(account_csv_fields, Account.constructor_parameters)


def accounts_from_csv(account_csv):
    items = []
    for row in DictReader(account_csv):
        account_args = csv_to_constructor.cast_from(row)
        items.append(Account(**account_args))

    collection = AccountCollection(items)
    return collection