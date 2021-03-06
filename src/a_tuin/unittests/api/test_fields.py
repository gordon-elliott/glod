__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""
from collections import OrderedDict
from unittest import TestCase

import graphene
from graphene import Node
from graphene.types.datetime import DateTime

from a_tuin.api.fields import get_local_fields, FieldNameReserved
from a_tuin.unittests.api.graphql_schema_test_case import GraphQLSchemaTestCase
from a_tuin.unittests.api.fixtures.leaves import AClassLeaf, AReferringClassLeaf
from a_tuin.unittests.api.fixtures.models import AClass, AClassStatus, ATypedClass


class TestFields(TestCase):

    def test_get_local_fields(self):
        expected = OrderedDict(
            (
                ('ref_no', graphene.Int),
                ('name', graphene.String),
                ('is_running', graphene.Boolean),
                ('date', DateTime),
            )
        )

        local_fields = get_local_fields(AClass)
        enum_field = local_fields.pop('status')
        actual = OrderedDict(
            (k, v.type)
            for k, v in local_fields.items()
        )

        self.assertEqual(expected, actual)
        self.assertEqual(AClassStatus, enum_field.type._meta.enum)

    def test_exception_on_reserved(self):
        with self.assertRaises(FieldNameReserved):
            get_local_fields(ATypedClass)


class RootQueryType(graphene.ObjectType):
    node = Node.Field()
    aclass = Node.Field(AClassLeaf)
    areferringclass = Node.Field(AReferringClassLeaf)


schema = graphene.Schema(query=RootQueryType)


class TestLeafNodes(GraphQLSchemaTestCase):

    def test_leaf_nodes(self):

        aclassleaf_tested = False
        areferringclass_tested = False

        for reported_type in self.get_types(schema):
            if reported_type['name'] == 'AClassLeaf':
                self.assertEqual(
                    ('id', 'refNo', 'name', 'isRunning', 'status', 'date'),
                    tuple(field['name'] for field in reported_type['fields'])
                )
                aclassleaf_tested = True
            if reported_type['name'] == 'AReferringClassLeaf':
                self.assertEqual(
                    ('id', 'name', 'aclass'),
                    tuple(field['name'] for field in reported_type['fields'])
                )
                self.assertEqual('AClassLeaf', reported_type['fields'][2]['type']['name'])
                areferringclass_tested = True

        self.assertTrue(aclassleaf_tested)
        self.assertTrue(areferringclass_tested)
