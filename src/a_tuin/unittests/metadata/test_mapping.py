__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from collections import OrderedDict
from decimal import Decimal
from unittest import TestCase

from a_tuin.metadata import prefix_name_with_underscore
from a_tuin.metadata.field import DateTimeField, DateField, DecimalField
from a_tuin.metadata.field_group import ListFieldGroup, PartialDictFieldGroup
from a_tuin.metadata.mapping import Mapping, IncompatibleFieldTypes
from a_tuin.unittests.metadata.fixture_field_group import (
    FIELD_COMBINATIONS,
    FIELDS,
    INITIAL_VALUES,
    field_group_combinations,
    inplace_field_group_combinations,
    DATETIME_FIXTURE
)


class TestMapping(TestCase):

    def test_invalid_type(self):
        for source_field_type, destination_field_type in (
            (DecimalField, DateTimeField),
            (DateTimeField, DecimalField),
            (DecimalField, DateField),
            (DateField, DecimalField),
        ):
            with self.subTest('{}, {}'.format(source_field_type, destination_field_type)):

                source_field_group = ListFieldGroup((source_field_type('source field'),))
                destination_field_group = ListFieldGroup((destination_field_type('dest field'),))
                with self.assertRaises(IncompatibleFieldTypes):
                    Mapping(source_field_group, destination_field_group)

    def test_reverse(self):
        for (_, source_field_group, _), (dest_field_group_class, _, _) in field_group_combinations():

            with self.subTest('{}, {}'.format(type(source_field_group), dest_field_group_class)):

                dest_field_group = source_field_group.derive(prefix_name_with_underscore, dest_field_group_class)
                mapping = Mapping(source_field_group, dest_field_group)

                self.assertEqual(
                    ['name', '_name'],
                    [f.name for f in mapping._field_mappings[0]]
                )

                reverse_mapping = mapping.reverse()

                self.assertEqual(
                    ['_name', 'name'],
                    [f.name for f in reverse_mapping._field_mappings[0]]
                )

    def test_update_in_place(self):
        destination_initial_values = {
            'name': 'revised name',
            'count': 9,
            'rate': 4940234.449994,
            'amount': Decimal('1000000.01'),
            'timestamp': DATETIME_FIXTURE
        }

        for (_, source_field_group, source_constructor), (_, dest_field_group, destination_constructor) in \
                inplace_field_group_combinations():

            with self.subTest('{}, {}'.format(type(source_field_group), type(dest_field_group))):

                # need to construct fixtures here as product() shares lists between
                # generated combinations thus test iterations were not independent
                source_instance = source_constructor(INITIAL_VALUES)
                destination_instance = destination_constructor(destination_initial_values)

                mapping = Mapping(source_field_group, dest_field_group)

                self.assertNotEqual(
                    source_field_group.as_dict(source_instance),
                    dest_field_group.as_dict(destination_instance)
                )

                mapping.update_in_place(source_instance, destination_instance)

                self.assertEqual(
                    source_field_group.as_dict(source_instance),
                    dest_field_group.as_dict(destination_instance)
                )

    def test_cast_from(self):
        for (_, source_field_group, source_constructor), (_, dest_field_group, destination_constructor) in \
                field_group_combinations():

            with self.subTest('{}, {}'.format(type(source_field_group), type(dest_field_group))):

                source_instance = source_constructor(INITIAL_VALUES)
                mapping = Mapping(source_field_group, dest_field_group)
                destination_instance = mapping.cast_from(source_instance)

                self.assertEqual(
                    INITIAL_VALUES,
                    dest_field_group.as_dict(destination_instance)
                )

    def test_valid_type_cast(self):
        source_fields, destination_fields = tuple(zip(*FIELD_COMBINATIONS))
        source_fields = tuple(set(source_fields))
        destination_fields = tuple(set(destination_fields))

        for (_, source_field_group, source_constructor), (_, dest_field_group, destination_constructor) in \
                field_group_combinations(source_fields, destination_fields):

            with self.subTest('{}, {}'.format(type(source_field_group), type(dest_field_group))):

                source_instance = source_constructor(INITIAL_VALUES)
                mapping = Mapping(source_field_group, dest_field_group)
                mapping.cast_from(source_instance)

    def test_partial_cast_from(self):

        source_field_group = PartialDictFieldGroup(FIELDS)
        dest_field_group = PartialDictFieldGroup(FIELDS)
        source_instance = INITIAL_VALUES.copy()
        del source_instance['name']
        del source_instance['timestamp']
        mapping = Mapping(source_field_group, dest_field_group)
        destination_instance = mapping.cast_from(source_instance)

        self.assertEqual(
            source_instance,
            dest_field_group.as_dict(destination_instance)
        )

    def test_cast_from_preserves_input_order(self):

        source_field_group = PartialDictFieldGroup(FIELDS)
        dest_field_group = PartialDictFieldGroup(FIELDS)
        source_instance = OrderedDict((
            ('rate', 1.243),
            ('count', 4),
            ('timestamp', DATETIME_FIXTURE),
        ))

        mapping = Mapping(source_field_group, dest_field_group)
        destination_instance = mapping.cast_from(source_instance)

        self.assertEqual(
            source_instance,
            destination_instance
        )
