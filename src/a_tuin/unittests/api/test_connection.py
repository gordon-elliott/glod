__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""
import graphene
from graphene import Node

from a_tuin.api.connection import node_connection_field
from a_tuin.unittests.api.graphql_schema_test_case import GraphQLSchemaTestCase
from a_tuin.unittests.api.fixtures.mapping import AClass, AClassQuery
from a_tuin.unittests.api.fixtures.nodes import AClassNode


aclass_connection_field = node_connection_field(
    AClass,
    AClassQuery,
    AClassNode,
    description="Fixture class"
)


class RootQueryType(graphene.ObjectType):
    node = Node.Field()
    aclasses = aclass_connection_field


schema = graphene.Schema(query=RootQueryType)


class TestConnection(GraphQLSchemaTestCase):

    def test_connection_field(self):

        root_tested = False
        filter_tested = False
        connection_tested = False
        edge_tested = False
        aclass_tested = False

        for reported_type in self.get_types(schema):
            if reported_type['name'] == 'RootQueryType':
                self.assertEqual(
                    (
                        ('filters', 'AClassFilterInput'),
                        ('before', 'String'),
                        ('after', 'String'),
                        ('first', 'Int'),
                        ('last', 'Int'),
                    ),
                    tuple(
                        (arg['name'], arg['type']['name'])
                        for arg in reported_type['fields'][0]['args']
                    )
                )
                root_tested = True
            if reported_type['name'] == 'AClassFilterInput':
                self.assertEqual(
                    (
                        ('refNo', 'Int'),
                        ('name', 'String'),
                        ('isRunning', 'Boolean'),
                        ('status', 'AClassStatus'),
                    ),
                    tuple(
                        (arg['name'], arg['type']['name'])
                        for arg in reported_type['inputFields']
                    )
                )
                filter_tested = True
            if reported_type['name'] == 'AClassNodeConnection':
                self.assertEqual(
                    ('pageInfo', 'edges', 'totalCount', 'filteredCount'),
                    tuple(field['name'] for field in reported_type['fields'])
                )
                self.assertEqual(
                    'AClassNodeEdge',
                    reported_type['fields'][1]['type']['ofType']['ofType']['name']
                )
                connection_tested = True
            if reported_type['name'] == 'AClassNodeEdge':
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

        self.assertTrue(root_tested)
        self.assertTrue(filter_tested)
        self.assertTrue(connection_tested)
        self.assertTrue(edge_tested)
        self.assertTrue(aclass_tested)

    def test_resolve_filter(self):
        # TODO start here
        # {'first': 7, 'filters': {'status': 1, 'name': 'somename'}}
        pass
