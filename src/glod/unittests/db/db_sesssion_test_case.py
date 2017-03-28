from unittest import TestCase

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from a_tuin.db.metadata import metadata
from glod.configuration import configuration


class DBSessionTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.engine = create_engine(configuration.db.connection_string, echo=True)

        # TODO create a new schema for each test run (not each suite)
        # TODO only create if schema is not present
        metadata.create_all(cls.engine)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        metadata.drop_all(cls.engine)

    def setUp(self):
        super().setUp()

        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()

    def tearDown(self):
        super().tearDown()

        self.session.close()