__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

import logging

from a_tuin.db.session_scope import session_scope
from a_tuin.db.metadata import truncate_tables, tables_in_dependency_order

from glod.configuration import configuration
from glod.db.engine import engine
from glod.db import ParishionerQuery
from glod.io.organisation import reorganise_parishioners


LOG = logging.getLogger(__file__)


def do_idl():
    LOG.info('Reorganising parishioner sheet')

    truncate_tables(
        engine,
        configuration.db.default_database_name,
        tables_in_dependency_order(('organisation', 'person', 'address', 'organisation_address'))
    )

    try:
        with session_scope() as session:
            parishioners = ParishionerQuery(session).collection()
            reorganise_parishioners(session, parishioners)
    except Exception as ex:
        LOG.exception(ex)


if __name__ == '__main__':
    do_idl()
