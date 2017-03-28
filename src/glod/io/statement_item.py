__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from csv import DictWriter, excel_tab

from a_tuin.metadata import StringField, DenormalisedField, DictFieldGroup, Mapping
from glod.model.statement_item import StatementItem


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