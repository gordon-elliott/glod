__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

from unittest import TestCase

from a_tuin.unittests.api.graphql_queries import SCHEMA_QUERY


class GraphQLSchemaTestCase(TestCase):

    def get_types(self, schema):
        result = schema.execute(SCHEMA_QUERY)

        assert result.errors == []

        reported_schema = result.data['__schema']
        return reported_schema['types']
