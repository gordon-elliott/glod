__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import logging

from sqlalchemy import MetaData
from contextlib import closing


LOG = logging.getLogger(__name__)
metadata = MetaData()


def tables_in_dependency_order(table_names=None):
    return (
        table.name
        for table in reversed(metadata.sorted_tables)
        if not table_names or table.name in table_names
    )


def truncate_tables(engine, db_name, tables_in_order):
    with closing(engine.connect()) as connection:
        transaction = connection.begin()
        connection.execute('TRUNCATE {} RESTART IDENTITY;'.format(
            ', '.join(tables_in_order)
        ))
        transaction.commit()
    LOG.info('Cleared tables in test DB %s', db_name)


def truncate_all(engine, db_name):
    truncate_tables(engine, db_name, tables_in_dependency_order())
