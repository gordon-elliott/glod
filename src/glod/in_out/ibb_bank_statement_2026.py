__copyright__ = 'Copyright(c) Gordon Elliott 2026'
""" 
"""
import logging

from csv import reader
from typing import Any

from a_tuin.metadata import StringField, ComputedStringField, ListFieldGroup, Mapping
from glod.model.statement_item import StatementItemDesignatedBalance
from glod.in_out.casts import cast_ymd_date_from_string, negate

LOG = logging.getLogger(__name__)


def _pick_field(
    field_group: ListFieldGroup, values_list: list, switch_fieldname: str, match_value: str, field_to_use: str
) -> Any:
    switch_field = field_group[switch_fieldname]
    switch_value = field_group._get_value(values_list, switch_field)
    if switch_value == match_value:
        field_to_use = field_group[field_to_use]
        return field_group._get_value(values_list, field_to_use)
    return None


class StatementLoader(object):
    def __init__(self, item_instance_class, account_collection):
        self._item_instance_class = item_instance_class
        self._account_collection = account_collection

        csv_field_account = StringField('account')
        csv_field_pending_historical = StringField('pending_historical')
        csv_field_amount = StringField('amount')
        csv_field_currency = StringField('currency')
        csv_field_debit_credit = StringField('debit_credit')
        csv_field_date = StringField('date')
        csv_field_narrative = StringField('narrative')
        csv_field_balance = StringField('balance')
        csv_field_balance_credit_debit = StringField('balance_credit_debit')
        csv_field_transaction_reference = StringField('transaction_reference')
        csv_creditor_name = StringField('creditor_name')
        csv_debtor_name = StringField('debtor_name')
        csv_field_debit = ComputedStringField(
            'debit', lambda fg, i: _pick_field(fg, i, 'debit_credit', 'Debit', 'amount')
        )
        csv_field_credit = ComputedStringField(
            'credit', lambda fg, i: _pick_field(fg, i, 'debit_credit', 'Credit', 'amount')
        )
        csv_field_detail_override = ComputedStringField('detail_override', lambda fg, i: None)
        csv_field_designated_balance = ComputedStringField(
            'designated_balance', lambda fg, i: StatementItemDesignatedBalance.No
        )

        statement_item_csv_fields = ListFieldGroup(
            (
                csv_field_account,
                csv_field_pending_historical,
                csv_field_amount,
                csv_field_currency,
                csv_field_debit_credit,
                csv_field_date,
                csv_field_narrative,
                csv_field_balance,
                csv_field_balance_credit_debit,
                csv_field_transaction_reference,
                csv_creditor_name,
                csv_debtor_name,
                csv_field_debit,
                csv_field_credit,
                csv_field_detail_override,
                csv_field_designated_balance
            )
        )

        field_mappings = tuple(
            zip(
                (
                    csv_field_account,
                    csv_field_date,
                    csv_field_narrative,
                    csv_field_currency,
                    csv_field_debit,
                    csv_field_credit,
                    csv_field_balance,
                    csv_field_detail_override,
                    csv_field_designated_balance
                ),
                item_instance_class.constructor_parameters
            )
        )

        self.csv_to_constructor = Mapping(
            statement_item_csv_fields,
            item_instance_class.constructor_parameters,
            field_mappings,
            field_casts=dict(
                date=cast_ymd_date_from_string,
                account=self._account_lookup,
                debit=negate,
            )
        )

    def _account_lookup(self, iban, *_):
        matching_accounts = list(self._account_collection.lookup(iban, 'canonical_IBAN'))
        if matching_accounts:
            return matching_accounts[0]
        raise KeyError('IBAN lookup failed for IBAN %s', iban)

    def _statement_line(self, line):
        kwargs = self.csv_to_constructor.cast_from(line)
        return self._item_instance_class(**kwargs)

    def _load_from_statement_original_order(self, csv_file):
        for line_number, line in enumerate(reader(csv_file)):
            try:
                if line_number > 0:
                    item_instance = self._statement_line(line)
                    if item_instance:
                        yield item_instance
            except Exception as ex:
                LOG.exception('Failed to load statement on line %d: %s', line_number, line)

    def load_from_statement(self, csv_file):
        yield from reversed(list(self._load_from_statement_original_order(csv_file)))
