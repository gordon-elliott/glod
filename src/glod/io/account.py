__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from csv import DictReader

from glod.model.account import Account
from glod.model.account_collection import AccountCollection

from glod.metadata import Mapping, DictFieldGroup


def replace_underscore_with_space(_, target):
    target._name = target._name.replace('_', ' ')

account_csv_fields = Account.constructor.derive(replace_underscore_with_space, DictFieldGroup)

csv_to_constructor = Mapping(account_csv_fields, Account.constructor)

def accounts_from_csv(account_csv):
    items = []
    for row in DictReader(account_csv):
        account_args = csv_to_constructor.cast_from(row)
        items.append(Account(**account_args))

    collection = AccountCollection(items)
    return collection