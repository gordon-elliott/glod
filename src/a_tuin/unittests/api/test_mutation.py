__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene

from a_tuin.api.mutations import get_create_mutation, get_update_mutation
from a_tuin.unittests.api.graphql_schema_test_case import GraphQLSchemaTestCase
from a_tuin.unittests.api.fixtures.models import AClass
from a_tuin.unittests.api.fixtures.leaves import aclass_fields, AClassLeaf


CreateAClassLeaf = get_create_mutation(AClass, aclass_fields, AClassLeaf)
UpdateAClassLeaf = get_update_mutation(AClass, aclass_fields, AClassLeaf)


class RootQueryType(graphene.ObjectType):
    node = graphene.Node.Field()


class Mutations(graphene.ObjectType):
    aclass_create = CreateAClassLeaf.Field()
    aclass_update = UpdateAClassLeaf.Field()


schema = graphene.Schema(query=RootQueryType, mutation=Mutations)


class TestMutation(GraphQLSchemaTestCase):

    def assertLeafPayload(self, reported_type):
        self.assertEqual(
            ('aclass', 'errors', 'clientMutationId'),
            tuple(field['name'] for field in reported_type['fields'])
        )
        self.assertEqual(
            'AClassLeaf',
            reported_type['fields'][0]['type']['name']
        )

    def test_mutation(self):

        mutatation_tested = False
        create_tested = False
        update_tested = False

        for reported_type in self.get_types(schema):
            if reported_type['name'] == 'Mutations':
                self.assertEqual(
                    (
                        ('aclassCreate', 'AClassCreateLeafPayload'),
                        ('aclassUpdate', 'AClassUpdateLeafPayload')
                    ),
                    tuple(
                        (field['name'], field['type']['name'])
                        for field in reported_type['fields']
                    )
                )
                mutatation_tested = True
            if reported_type['name'] == 'AClassCreateLeafPayload':
                self.assertLeafPayload(reported_type)
                create_tested = True
            if reported_type['name'] == 'AClassUpdateLeafPayload':
                self.assertLeafPayload(reported_type)
                update_tested = True

        self.assertTrue(mutatation_tested)
        self.assertTrue(create_tested)
        self.assertTrue(update_tested)
