__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" Initial data load for CCD data
"""

import logging

from a_tuin.db.metadata import truncate_tables, tables_in_dependency_order


from glod.configuration import configuration
from glod.db.engine import engine
from glod.io.idl_ccd_parish_list import load_parish_list, DEPENDENT_TABLES as PARISH_LIST_TABLES
from glod.io.idl_ccd_parishioners import transform_parishioners, DEPENDENT_TABLES as PARISHIONERS_TABLES
from glod.io.idl_ccd_detailed_ledger import load_detailed_ledger, DEPENDENT_TABLES as LEDGER_TABLES


LOG = logging.getLogger(__file__)


def do_idl():
    tables = {PARISH_LIST_TABLES + PARISHIONERS_TABLES + LEDGER_TABLES}
    truncate_tables(
        engine,
        configuration.db.operational_db_name,
        tables_in_dependency_order(*tables)
    )

    load_parish_list()
    transform_parishioners()
    load_detailed_ledger()


if __name__ == '__main__':
    do_idl()
