__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

import logging
import pkg_resources

from functools import partial

from a_tuin.db.metadata import metadata, truncate_tables, tables_in_dependency_order
from a_tuin.db.session_scope import session_scope
from a_tuin.io.google_sheets import configure_client, extract_table

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


def do_idl():
    sheets_config = configuration.google_sheets
    credentials_path = pkg_resources.resource_filename(
        __name__,
        '../config/{}'.format(sheets_config.credentials_file)
    )
    google_sheets_client = configure_client(credentials_path)
    spreadsheet = google_sheets_client.open_by_key(sheets_config.ledger_sheet_id)
    extract_from_detailed_ledger = partial(extract_table, spreadsheet)
    LOG.info('Extracting data from %s (%s)', spreadsheet.title, sheets_config.ledger_sheet_id)

    truncate_tables(
        engine,
        configuration.db.default_database_name,
        tables_in_dependency_order((
            'account', 'fund', 'nominal_account', 'subject',
            'counterparty', 'envelope', 'pps',
            'statement_item',
            'transaction', 'transaction_check'
        ))
    )

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


if __name__ == '__main__':
    do_idl()
