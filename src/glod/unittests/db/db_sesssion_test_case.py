from unittest import TestCase

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from glod.configuration import configuration
from glod.db.metadata import metadata


class DBSessionTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.engine = create_engine(configuration.db.connection_string, echo=True)

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