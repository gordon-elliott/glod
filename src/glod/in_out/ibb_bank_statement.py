__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""
import logging

from csv import reader

from a_tuin.db.session_scope import session_scope
from a_tuin.metadata import StringField, UnusedField, ComputedStringField, ListFieldGroup, Mapping
from glod.db import AccountQuery
from glod.in_out.account import accounts_from_csv
from glod.in_out.statement_item import cast_dmy_date_from_string, statement_item_to_gsheet, statement_item_csv
from glod.model.statement_item import StatementItemDesignatedBalance


LOG = logging.getLogger(__name__)


def get_account_collection(account_file):
    if account_file:
        account_collection = accounts_from_csv(account_file)
    else:
        with session_scope() as session:
            account_collection = AccountQuery(session).collection()
    return account_collection


def output_statement_items(output_csv, output_gsheet, statement_items):
    if output_gsheet:
        LOG.info(f"Writing to gsheet {output_gsheet}")
        statement_item_to_gsheet(statement_items, output_gsheet)
    elif output_csv:
        with output_csv:
            statement_item_csv(statement_items, output_csv)
    else:
        with session_scope() as session:
            for statement_item in statement_items:
                session.add(statement_item)


class StatementLoader(object):
    def __init__(self, item_instance_class, account_collection):
        self._item_instance_class = item_instance_class
        self._account_collection = account_collection

        csv_field_account = StringField('account')
        csv_field_date = StringField('date')
        csv_field_details = StringField('details')
        csv_field_currency = StringField('currency')
        csv_field_debit = StringField('debit')
        csv_field_credit = StringField('credit')
        csv_field_balance = StringField('balance')
        csv_field_detail_override = ComputedStringField('detail_override', lambda fg, i: None)
        csv_field_designated_balance = ComputedStringField('designated_balance', lambda fg, i: StatementItemDesignatedBalance.No)

        statement_item_csv_fields = ListFieldGroup(
            (
                csv_field_account,
                UnusedField('_unused_'),
                csv_field_date,
                UnusedField('_unused_'),
                csv_field_details,
                csv_field_currency,
                csv_field_debit,
                csv_field_credit,
                csv_field_balance,
                csv_field_detail_override,
                csv_field_designated_balance
            )
        )

        field_mappings = tuple(zip(
            (
                csv_field_account,
                csv_field_date,
                csv_field_details,
                csv_field_currency,
                csv_field_debit,
                csv_field_credit,
                csv_field_balance,
                csv_field_detail_override,
                csv_field_designated_balance
            ),
            item_instance_class.constructor_parameters
        ))

        self.csv_to_constructor = Mapping(
            statement_item_csv_fields,
            item_instance_class.constructor_parameters,
            field_mappings,
            field_casts=dict(date=cast_dmy_date_from_string)
        )

    def _account_header(self, line):
        account_no = line[3]
        self._account = list(self._account_collection.lookup(account_no, '_account_no'))[0]
        return None

    def _statement_line(self, line):
        kwargs = self.csv_to_constructor.cast_from([self._account] + line)
        return self._item_instance_class(**kwargs)

    def _eof(self, line):
        return None

    LINE_TYPE_MAP = {
        '01': _account_header,
        '02': _statement_line,
        '99': _eof,
    }

    def load_from_statement(self, csv_file):
        for line in reader(csv_file):
            line_type = line[0]
            processor = self.LINE_TYPE_MAP[line_type]
            item_instance = processor(self, line)
            if item_instance:
                yield item_instance
