__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""
import graphene
from graphene import Node

from a_tuin.api.connection import node_connection_field
from a_tuin.unittests.api.graphql_schema_test_case import GraphQLSchemaTestCase
from a_tuin.unittests.api.fixtures.mapping import AClassQuery
from a_tuin.unittests.api.fixtures.nodes import AClassNode


aclasss_connection_field = node_connection_field(
    AClassQuery,
    AClassNode,
    description="Fixture class"
)


class RootQueryType(graphene.ObjectType):
    node = Node.Field()
    accounts = aclasss_connection_field


schema = graphene.Schema(query=RootQueryType)


class TestConnection(GraphQLSchemaTestCase):

    def test_connection_field(self):

        connection_tested = False
        edge_tested = False
        aclass_tested = False

        for reported_type in self.get_types(schema):
            if reported_type['name'] == 'AClassQueryNodeConnection':
                self.assertEqual(
                    ('pageInfo', 'edges', 'totalCount', 'filteredCount'),
                    tuple(field['name'] for field in reported_type['fields'])
                )
                self.assertEqual(
                    'AClassQueryNodeEdge',
                    reported_type['fields'][1]['type']['ofType']['ofType']['name']
                )
                connection_tested = True
            if reported_type['name'] == 'AClassQueryNodeEdge':
                self.assertEqual(
                    'AClassNode',
                    reported_type['fields'][0]['type']['name']
                )
                edge_tested = True
            if reported_type['name'] == 'AClassNode':
                self.assertEqual(
                    ('id', 'refNo', 'name', 'isRunning', 'status', 'refers'),
                    tuple(field['name'] for field in reported_type['fields'])
                )
                aclass_tested = True

        self.assertTrue(connection_tested)
        self.assertTrue(edge_tested)
        self.assertTrue(aclass_tested)
