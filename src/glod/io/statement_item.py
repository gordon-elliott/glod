__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from csv import DictWriter, excel_tab
from datetime import date, datetime

from a_tuin.metadata import StringField, DenormalisedField, DictFieldGroup, Mapping
from a_tuin.io.gsheet_integration import get_gsheet_fields, load_class
from glod.io.casts import strip_commas
from glod.db.statement_item import StatementItem, StatementItemDesignatedBalance

from glod.db.account import AccountQuery


def statement_item_csv(statement_items, csv_file):

    field_names = tuple(
        field.name
        for field in StatementItem.constructor_parameters
    )

    def extract_account_no(account):
        return account._account_no

    csv_fields = tuple(
        DenormalisedField(name, extract_account_no) if name == 'account' else StringField(name)
        for name in field_names
    )
    csv_fields[1]._strfmt = '%d/%m/%Y'
    csv_field_group = DictFieldGroup(csv_fields)

    internal_to_csv = Mapping(StatementItem.internal, csv_field_group)

    csv_writer = DictWriter(csv_file, field_names, dialect=excel_tab)
    csv_writer.writeheader()

    for statement_item in statement_items:
        csv_writer.writerow(
            internal_to_csv.cast_from(statement_item)
        )

    return csv_file


def ignore_na(value, _):
    if value == 'N/A':
        return None
    else:
        return strip_commas(value, _)


def cast_dmy_date_from_string(value, _):
    return date.fromtimestamp(datetime.strptime(value, '%d/%m/%Y').timestamp())


def cast_designated_balance(value, _):
    if not value:
        return StatementItemDesignatedBalance.No
    elif value.lower() == 'opening':
        return StatementItemDesignatedBalance.Opening
    else:
        return StatementItemDesignatedBalance.Closing


def statement_item_from_gsheet(session, extract_from_detailed_ledger):

    statement_item_gsheet = get_gsheet_fields(StatementItem, None)
    field_casts = {
        'account': AccountQuery(session).instance_finder('account_no', None),
        'date': cast_dmy_date_from_string,
        'debit': strip_commas,
        'credit': strip_commas,
        'balance': ignore_na,
        'designated balance': cast_designated_balance,
    }
    statement_item_mapping = Mapping(statement_item_gsheet, StatementItem.constructor_parameters, field_casts=field_casts)
    statement_items = extract_from_detailed_ledger(
        'bank statements',
        'A1',
        ('account', 'date', 'details', 'currency', 'debit', 'credit', 'balance', 'detail override', 'designated balance')
    )
    load_class(session, statement_items, statement_item_mapping, StatementItem)
