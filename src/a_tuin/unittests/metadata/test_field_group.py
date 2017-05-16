__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""
from datetime import datetime
from decimal import Decimal
from unittest import TestCase

from a_tuin.metadata import prefix_name_with_underscore
from a_tuin.metadata.field import StringField
from a_tuin.metadata.exceptions import RequiredValueMissing
from a_tuin.metadata.field_group import (
    ListFieldGroup, PartialDictFieldGroup
)
from a_tuin.unittests.metadata.fixture_field_group import (
    field_group_fixtures,
    FIELDS,
    INITIAL_VALUES,
    MUTABLE_FIELD_GROUP_CLASSES,
    DATETIME_FIXTURE
)


class TestFieldList(TestCase):

    def test_iteration(self):
        for _, field_group, _ in field_group_fixtures():
            self.assertListEqual(
                [
                    ('name', str),
                    ('count', int),
                    ('rate', float),
                    ('amount', Decimal),
                    ('timestamp', datetime)
                ],
                [(field.name, field._type) for field in field_group]
            )

    def test_derivation(self):

        for _, field_group, _ in field_group_fixtures():
            internal = field_group.derive(prefix_name_with_underscore)
            self.assertIsInstance(internal, type(field_group))

            for internal_item, public_item in zip(internal, field_group):
                self.assertEqual(
                    '_' + public_item._name,
                    internal_item._name
                )

    def test_filled_instance(self):

        for _, field_group, constructor in field_group_fixtures():
            new_instance = field_group.fill_instance_from_dict(INITIAL_VALUES)
            self.assertEqual(
                INITIAL_VALUES,
                field_group.as_dict(new_instance)
            )

    def test_get_value(self):

        for _, field_group, constructor in field_group_fixtures():
            for field in field_group:
                self.assertEqual(
                    INITIAL_VALUES[field.name],
                    field_group.get_value(constructor(INITIAL_VALUES), field)
                )

    def test_as_dict(self):

        for _, field_group, constructor in field_group_fixtures():
            self.assertEqual(
                INITIAL_VALUES,
                field_group.as_dict(constructor(INITIAL_VALUES))
            )

    def test_set_value(self):

        updates = {
            'name': 'revised name',
            'count': 9,
            'rate': 4940234.449994,
            'amount': Decimal('1000000.01'),
            'timestamp': DATETIME_FIXTURE
        }

        for field_group_class, field_group, constructor in field_group_fixtures(
                field_group_classes=MUTABLE_FIELD_GROUP_CLASSES
        ):
            instance = constructor(INITIAL_VALUES)
            for field in field_group:
                self.assertEqual(
                    INITIAL_VALUES[field.name],
                    field_group.get_value(instance, field)
                )

                field_group.set_value(instance, field, updates[field.name])

                self.assertEqual(
                    updates[field.name],
                    field_group.get_value(instance, field)
                )

    def test_set_update_none(self):

        field = StringField('fixture', required=True)
        field_group = ListFieldGroup((field,))
        instance = field_group.empty_instance()

        with self.assertRaises(RequiredValueMissing):
            field_group.set_value(instance, field, None)

    def test_set_update_default(self):

        default_fixture = 'default'
        field = StringField('fixture', required=True, default=default_fixture)
        field_group = ListFieldGroup((field,))
        instance = field_group.empty_instance()

        field_group.set_value(instance, field, None)
        self.assertEqual(
            default_fixture,
            field_group.get_value(instance, field)
        )

    def test_instances_differ_no_differences(self):

        for _, field_group, constructor in field_group_fixtures():
            instance = field_group.fill_instance_from_dict(INITIAL_VALUES)
            other = field_group.fill_instance_from_dict(INITIAL_VALUES)
            self.assertFalse(
                field_group.instances_differ(instance, other)
            )

    def test_instances_differ_differences_exist(self):
        modified = INITIAL_VALUES.copy()
        modified['amount'] = Decimal('3.99')
        for _, field_group, constructor in field_group_fixtures():
            instance = field_group.fill_instance_from_dict(INITIAL_VALUES)
            other = field_group.fill_instance_from_dict(modified)
            self.assertTrue(
                field_group.instances_differ(instance, other)
            )

class TestPartialDictFieldGroup(TestCase):

    def test_fill_instance_from_dict(self):
        modified = INITIAL_VALUES.copy()
        del modified['count']
        del modified['timestamp']
        field_group = PartialDictFieldGroup(FIELDS)

        filled = field_group.fill_instance_from_dict(modified)

        self.assertEqual(modified, filled)
