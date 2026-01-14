__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from csv import DictReader

from a_tuin.in_out.gsheet_integration import get_gsheet_fields, load_class
from a_tuin.in_out.google_sheets import extract_from_sheet
from a_tuin.metadata import (
    Mapping,
    DictFieldGroup,
    StringField,
    replace_underscore_with_space
)
from glod.model.account import AccountStatus, Account, AccountCollection

ACCOUNT_FIELD_NAMES = ('id', 'purpose', 'status', 'name', 'institution', 'sort code', 'account no', 'BIC', 'IBAN')
ACCOUNT_STATUS_MAP = {
    'in use': AccountStatus.Active,
    'ready': AccountStatus.Active,
    'closed': AccountStatus.Closed,
}


def conform_value(value, _):
    return ACCOUNT_STATUS_MAP.get(value.lower(), AccountStatus.Active)


field_casts = dict(status=conform_value)

account_csv_fields = Account.constructor_parameters.derive(
    replace_underscore_with_space,
    DictFieldGroup
)
account_csv_fields['reference no'].name = 'id'
account_csv_fields['status'] = StringField('status')

csv_to_constructor = Mapping(account_csv_fields, Account.constructor_parameters, field_casts=field_casts)


def accounts_from_csv(account_csv):
    items = []
    for row in DictReader(account_csv):
        account_args = csv_to_constructor.cast_from(row)
        items.append(Account(**account_args))

    collection = AccountCollection(items)
    return collection


def accounts_from_gsheet(session, extract_from_detailed_ledger):
    account_gsheet = get_gsheet_fields(Account, {'reference no': 'id'})
    account_gsheet['status'] = StringField('status')
    account_mapping = Mapping(account_gsheet, Account.constructor_parameters, field_casts=field_casts)
    accounts = extract_from_detailed_ledger(
        'bank accounts',
        'A1',
        ('id', 'purpose', 'status', 'name', 'institution', 'sort code', 'account no', 'BIC', 'IBAN')
    )
    load_class(session, accounts, account_mapping, Account)


def get_account_collection(account_file):
    if account_file:
        account_collection = accounts_from_csv(account_file)
        return account_collection


def get_accounts_from_sheet(configuration):
    extract_from_detailed_ledger = extract_from_sheet(configuration, configuration.gdrive.ledger_sheet_id)
    accounts = extract_from_detailed_ledger('bank accounts', 'A1', ACCOUNT_FIELD_NAMES)
    items = []
    for row_tuple in accounts:
        row = dict(zip(ACCOUNT_FIELD_NAMES, row_tuple))
        account_args = csv_to_constructor.cast_from(row)
        items.append(Account(**account_args))

    collection = AccountCollection(items)
    return collection
