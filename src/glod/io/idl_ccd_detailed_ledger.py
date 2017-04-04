__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

import logging
import pkg_resources

from functools import partial

from a_tuin.db.metadata import metadata, truncate_all
from a_tuin.db.session_scope import session_scope
from a_tuin.io.google_sheets import configure_client, extract_table

from glod.configuration import configuration
from glod.db.engine import engine
from glod.io.account import accounts_from_gsheet
from glod.io.fund import funds_from_gsheet


LOG = logging.getLogger(__file__)


def do_idl():
    metadata.create_all(engine)

    sheets_config = configuration.google_sheets
    credentials_path = pkg_resources.resource_filename(
        __name__,
        '../config/{}'.format(sheets_config.credentials_file)
    )
    google_sheets_client = configure_client(credentials_path)
    spreadsheet = google_sheets_client.open_by_key(sheets_config.idl_sheet_id)
    extract_from_detailed_ledger = partial(extract_table, spreadsheet)
    LOG.info('Extracting data from %s (%s)', spreadsheet.title, sheets_config.idl_sheet_id)

    truncate_all(engine, configuration.db.default_database_name)

    with session_scope() as session:
        accounts_from_gsheet(session, extract_from_detailed_ledger)
        funds_from_gsheet(session, extract_from_detailed_ledger)


# parishioners = extract_from_detailed_ledger('parishioners', 'A1', ('ID', 'SURNAME', 'FIRST_NAME', 'TITLE', 'SPOUSE', 'ADDRESS1', 'ADDRESS2', 'ADDRESS3', 'County', 'EIRCODE', 'CHILD_1', 'DOB1', 'CHILD_2', 'DOB2', 'CHILD_3', 'DOB3', 'child 4', 'DOB 4', 'TELEPHONE', 'GIVING', 'email'))
# subjects = extract_from_detailed_ledger('report lookups', 'A3', ('subject', 'select vestry summary', 'easter vestry summary', 'rcb code'))

do_idl()