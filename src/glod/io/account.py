__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from csv import DictReader

from glod.model.account import Account
from glod.model.account_collection import AccountCollection

from glod.metadata import (
    Mapping,
    DictFieldGroup,
    IntField,
    UnusedField,
    replace_underscore_with_space
)


account_csv_fields = Account.constructor_parameters.derive(
    replace_underscore_with_space,
    DictFieldGroup
)

field_mappings = [
     (IntField('id'), UnusedField('automatically assigned'))
 ] + list(zip(account_csv_fields, Account.constructor_parameters))

csv_to_constructor = Mapping(account_csv_fields, Account.constructor_parameters, field_mappings)


def accounts_from_csv(account_csv):
    items = []
    for row in DictReader(account_csv):
        account_args = csv_to_constructor.cast_from(row)
        items.append(Account(**account_args))

    collection = AccountCollection(items)
    return collection