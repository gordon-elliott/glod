__copyright__ = 'Copyright(c) Gordon Elliott 2018'

""" 
"""
from graphene.test import Client
from snapshottest import TestCase

from a_tuin.unittests.api.graphql_queries import SCHEMA_QUERY
from glod.api.schema import schema


class APISnapshotTestCase(TestCase):
    def test_schema(self):
        """ Testing the full schema metadata
        """
        client = Client(schema)
        self.assertMatchSnapshot(client.execute(SCHEMA_QUERY))
