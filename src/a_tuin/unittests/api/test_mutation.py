__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene

from datetime import date, datetime
from unittest.mock import Mock, patch

from a_tuin.api import get_local_fields
from a_tuin.api.mutations import get_create_mutation, get_update_mutation
from a_tuin.unittests.api.graphql_schema_test_case import GraphQLSchemaTestCase
from a_tuin.unittests.api.fixtures.models import AClass, AClassStatus
from a_tuin.unittests.api.fixtures.leaves import AClassLeaf


aclass_fields = get_local_fields(AClass)
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
            ('aClass', 'errors', 'clientMutationId'),
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

    def test_create(self):

        mock_session = Mock()
        context = {'request': {'session': mock_session}}

        mock_info = Mock()
        mock_info.field_name = 'AClassLeaf'
        mock_info.context = context

        ref_no = '7000'
        name = 'a name'
        is_running = 'True'
        status = 1
        date_string = '2019-03-19'
        date_value = date.fromtimestamp(datetime.strptime(date_string, '%Y-%m-%d').timestamp())

        input_dict = dict(
            ref_no=ref_no,
            name=name,
            is_running=is_running,
            status=status,
            date=date_value,
            clientMutationId=Mock(),
        )

        leaf = CreateAClassLeaf.mutate_and_get_payload('root_fixture', mock_info, **input_dict)

        self.assertEqual('AClassCreateLeaf', type(leaf).__name__)

        instance = mock_session.add.call_args[0][0]
        self.assertEqual(AClass, type(instance))

        self.assertEqual(int(ref_no), instance.ref_no)
        self.assertEqual(name, instance.name)
        self.assertEqual(True, instance.is_running)
        self.assertEqual(AClassStatus.Open, instance.status)
        self.assertEqual(date_value, instance.date)

    @patch('a_tuin.api.mutations.graphene.Node.get_node_from_global_id')
    def test_update(self, mock_get_from_id):

        initial_name = 'some name'
        id_ = 9989
        mock_get_from_id.return_value = mock_instance = AClass(name=initial_name, is_running=False)

        mock_session = Mock()
        context = {'request': {'session': mock_session}}

        mock_info = Mock()
        mock_info.field_name = 'AClassLeaf'
        mock_info.context = context

        ref_no = '7000'
        is_running = 'True'
        status = 1
        date_string = '2019-03-19'
        date_value = date.fromtimestamp(datetime.strptime(date_string, '%Y-%m-%d').timestamp())

        input_dict = dict(
            ref_no=ref_no,
            is_running=is_running,
            status=status,
            date=date_value,
            clientMutationId=Mock(),
            id=id_,
        )

        leaf = UpdateAClassLeaf.mutate_and_get_payload('root_fixture', mock_info, **input_dict)

        self.assertEqual('AClassUpdateLeaf', type(leaf).__name__)
        mock_get_from_id.assert_called_once_with(id_, context, mock_info)

        instance = leaf.aClass
        self.assertEqual(mock_instance, instance)

        self.assertEqual(int(ref_no), instance.ref_no)
        self.assertEqual(initial_name, instance.name)
        self.assertEqual(True, instance.is_running)
        self.assertEqual(AClassStatus.Open, instance.status)
        self.assertEqual(date_value, instance.date)
