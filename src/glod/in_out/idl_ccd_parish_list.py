__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

import logging

from a_tuin.db.metadata import truncate_tables, tables_in_dependency_order
from a_tuin.db.session_scope import session_scope
from a_tuin.in_out.google_sheets import extract_from_sheet

from glod.configuration import configuration
from glod.db.engine import engine
from glod.in_out.parish_list.parishioner import parishioners_from_gsheet
from glod.in_out.parish_list.household import households_from_gsheet


LOG = logging.getLogger(__file__)
DEPENDENT_TABLES = ('parishioner', 'household')


def load_parish_list():
    sheets_config = configuration.gdrive
    sheet_id = sheets_config.parish_list_sheet_id
    extract_from_parish_list = extract_from_sheet(configuration, sheet_id)

    try:
        with session_scope() as session:
            households_from_gsheet(session, extract_from_parish_list)
            parishioners_from_gsheet(session, extract_from_parish_list)
    except Exception as ex:
        LOG.exception(ex)


def do_idl():
    LOG.info('Load parish list from spreadsheet into staging tables')

    truncate_tables(
        engine,
        configuration.db.operational_db_name,
        tables_in_dependency_order(DEPENDENT_TABLES)
    )

    load_parish_list()


if __name__ == '__main__':
    do_idl()
