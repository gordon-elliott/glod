__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

import logging
import pkg_resources

from functools import partial

from a_tuin.db.metadata import truncate_tables, tables_in_dependency_order, metadata
from a_tuin.db.session_scope import session_scope
from a_tuin.io.google_sheets import configure_client, extract_table

from glod.configuration import configuration
from glod.db.engine import engine
from glod.io.parish_list.parishioner import parishioners_from_gsheet
from glod.io.parish_list.household import households_from_gsheet


LOG = logging.getLogger(__file__)


def do_idl():
    LOG.info('Load parish list from spreadsheet into staging tables')
    metadata.create_all(engine)

    sheets_config = configuration.google_sheets
    credentials_path = pkg_resources.resource_filename(
        __name__,
        '../config/{}'.format(sheets_config.credentials_file)
    )
    google_sheets_client = configure_client(credentials_path)
    spreadsheet = google_sheets_client.open_by_key(sheets_config.parish_list_sheet_id)
    extract_from_parish_list = partial(extract_table, spreadsheet)
    LOG.info('Extracting data from %s (%s)', spreadsheet.title, sheets_config.ledger_sheet_id)

    truncate_tables(
        engine,
        configuration.db.default_database_name,
        tables_in_dependency_order(('parishioner', 'household'))
    )

    try:
        with session_scope() as session:
            households_from_gsheet(session, extract_from_parish_list)
            parishioners_from_gsheet(session, extract_from_parish_list)
    except Exception as ex:
        LOG.exception(ex)


if __name__ == '__main__':
    do_idl()
