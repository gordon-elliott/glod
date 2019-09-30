__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

import logging

from a_tuin.db.metadata import truncate_tables, tables_in_dependency_order
from a_tuin.db.session_scope import session_scope
from a_tuin.io.google_sheets import extract_from_sheet

from glod.configuration import configuration
from glod.db.engine import engine
from glod.io.account import accounts_from_gsheet
from glod.io.fund import funds_from_gsheet
from glod.io.nominal_account import nominal_accounts_from_gsheet
from glod.io.subject import subjects_from_gsheet
from glod.io.statement_item import statement_item_from_gsheet
from glod.io.counterparty import counterparty_from_gsheet
from glod.io.envelope import envelopes_from_gsheet
from glod.io.pps import ppses_from_gsheet
from glod.io.transaction import transactions_from_gsheet


LOG = logging.getLogger(__file__)
DEPENDENT_TABLES = (
    'account', 'fund', 'nominal_account', 'subject',
    'counterparty', 'envelope', 'pps',
    'statement_item',
    'transaction', 'transaction_check'
)


def load_detailed_ledger():
    sheets_config = configuration.google_sheets
    sheet_id = sheets_config.ledger_sheet_id
    extract_from_detailed_ledger = extract_from_sheet(__name__, sheets_config, sheet_id)

    try:
        with session_scope() as session:
            accounts_from_gsheet(session, extract_from_detailed_ledger)
            funds_from_gsheet(session, extract_from_detailed_ledger)
            nominal_accounts_from_gsheet(session, extract_from_detailed_ledger)
            subjects_from_gsheet(session, extract_from_detailed_ledger)
            counterparty_from_gsheet(session, extract_from_detailed_ledger)
            envelopes_from_gsheet(session, extract_from_detailed_ledger)
            ppses_from_gsheet(session, extract_from_detailed_ledger)
            statement_item_from_gsheet(session, extract_from_detailed_ledger)
            transactions_from_gsheet(session, extract_from_detailed_ledger)
    except Exception as ex:
        LOG.exception(ex)


def do_idl():
    truncate_tables(
        engine,
        configuration.db.operational_db_name,
        tables_in_dependency_order(DEPENDENT_TABLES)
    )

    load_detailed_ledger()


if __name__ == '__main__':
    do_idl()
