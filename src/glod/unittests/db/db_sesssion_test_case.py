__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""
import logging
from unittest import TestCase
from uuid import uuid1

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database

from a_tuin.db.metadata import metadata, truncate_all
from glod.configuration import configuration


TEST_DB_NAME = 'test_{}'.format(uuid1().hex)
DB_NAME_FILE = '/tmp/glod_unittest_db_name.txt'
LOG = logging.getLogger(__name__)


class DBSessionTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        connection_string = configuration.db.connection_template.format(TEST_DB_NAME)

        cls.engine = create_engine(connection_string, echo=False)   # to avoid duplicate log messages
        if not database_exists(cls.engine.url):
            LOG.info('Creating test DB %s' % TEST_DB_NAME)
            create_database(cls.engine.url)

            metadata.create_all(cls.engine)

            # Make sure old test dbs are cleaned up
            with open(DB_NAME_FILE, 'r') as db_name_file:

                for old_db_name in db_name_file:
                    LOG.info('Dropping old test database {}'.format(old_db_name))
                    drop_database(
                        configuration.db.connection_template.format(old_db_name)
                    )

            with open(DB_NAME_FILE, 'w') as db_name_file:

                db_name_file.write('{}\n'.format(TEST_DB_NAME))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        truncate_all(cls.engine, TEST_DB_NAME)

    def setUp(self):
        super().setUp()

        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()

    def tearDown(self):
        super().tearDown()

        self.session.close()
