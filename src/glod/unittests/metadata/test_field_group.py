__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""
from datetime import datetime
from decimal import Decimal
from unittest import TestCase

from glod.metadata.field_group import prefix_name_with_underscore
from glod.unittests.metadata.fixture_field_group import (
    field_group_fixtures,
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
                [(field._name, field._type) for field in field_group]
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
                    INITIAL_VALUES[field._name],
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
                    INITIAL_VALUES[field._name],
                    field_group.get_value(instance, field)
                )

                field_group.set_value(instance, field, updates[field._name])

                self.assertEqual(
                    updates[field._name],
                    field_group.get_value(instance, field)
                )
