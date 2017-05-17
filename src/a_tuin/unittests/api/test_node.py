__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene
from graphene import Node

from a_tuin.unittests.api.graphql_schema_test_case import GraphQLSchemaTestCase
from a_tuin.unittests.api.fixtures.nodes import AClassNode


class RootQueryType(graphene.ObjectType):
    node = Node.Field()
    aclass = Node.Field(AClassNode)


schema = graphene.Schema(query=RootQueryType)


class TestNode(GraphQLSchemaTestCase):

    def test_node(self):
        aclass_tested = False

        for reported_type in self.get_types(schema):
            if reported_type['name'] == 'AClassNode':
                self.assertEqual(
                    ('id', 'refNo', 'name', 'isRunning', 'status', 'date', 'refers'),
                    tuple(field['name'] for field in reported_type['fields'])
                )
                aclass_tested = True

        self.assertTrue(aclass_tested)
