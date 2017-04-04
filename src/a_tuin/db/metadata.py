__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import logging

from sqlalchemy import MetaData
from contextlib import closing


LOG = logging.getLogger(__name__)
metadata = MetaData()


def truncate_all(engine, db_name):
    with closing(engine.connect()) as connection:
        transaction = connection.begin()
        connection.execute('TRUNCATE {} RESTART IDENTITY;'.format(
            ', '.join(table.name for table in reversed(metadata.sorted_tables))
        ))
        transaction.commit()
        LOG.info('Cleared all tables in test DB %s' % db_name)