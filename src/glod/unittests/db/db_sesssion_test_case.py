__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""
import logging
import os

from unittest import TestCase, skip
from uuid import uuid1

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database

from a_tuin.db.metadata import metadata, truncate_all
from glod.configuration import configuration
from glod.db.constants import SCHEMA_NAME as GLOD_SCHEMA
from a_tuin.unittests.api.fixtures.mapping import SCHEMA_NAME as ATUIN_SCHEMA


TEST_DB_NAME = 'test_{}'.format(uuid1().hex)
DB_NAME_FILE = '/tmp/glod_unittest_db_name.txt'
LOG = logging.getLogger(__name__)


# @skip("Not connected to db")
class DBSessionTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        connection_string = cls._test_db_connection_string(TEST_DB_NAME)
        cls.engine = create_engine(connection_string, echo=False)   # to avoid duplicate log messages

        if not database_exists(cls.engine.url):
            LOG.info('Creating test DB %s' % TEST_DB_NAME)
            create_database(cls.engine.url)
            for schema_name in (GLOD_SCHEMA, ATUIN_SCHEMA):
                cls.engine.execute("create schema {}".format(schema_name))

            metadata.create_all(cls.engine)

            # Make sure old test dbs are cleaned up
            if os.path.exists(DB_NAME_FILE):
                with open(DB_NAME_FILE, 'r') as db_name_file:

                    for old_db_name in db_name_file:
                        LOG.info('Dropping old test database {}'.format(old_db_name))
                        connection_string = cls._test_db_connection_string(old_db_name)
                        drop_database(connection_string)

            with open(DB_NAME_FILE, 'w') as db_name_file:
                db_name_file.write('{}\n'.format(TEST_DB_NAME))

    @classmethod
    def _test_db_connection_string(cls, db_name):
        db_configuration_map = configuration.db.toDict()
        db_configuration_map['operational_db_name'] = db_name
        connection_string = configuration.db.restricted_connection.format(**db_configuration_map)
        return connection_string

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
