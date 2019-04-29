__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from collections import OrderedDict
from decimal import Decimal
from unittest import TestCase
from unittest.mock import patch

from a_tuin.metadata import prefix_name_with_underscore
from a_tuin.metadata.field import DateTimeField, DateField, DecimalField
from a_tuin.metadata.field_group import ListFieldGroup, PartialDictFieldGroup
from a_tuin.metadata.mapping import Mapping, IncompatibleFieldTypes
from a_tuin.metadata.exceptions import FieldErrors
from a_tuin.unittests.metadata.fixture_field_group import (
    FIELD_COMBINATIONS,
    FIELDS,
    INITIAL_VALUES,
    field_group_combinations,
    inplace_field_group_combinations,
    DATETIME_FIXTURE,
    EXPECTED_VALUES
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
        destination_expected_values = INITIAL_VALUES.copy()
        destination_expected_values['dunder'] = "__computed__"

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

                destination_expected_instance = destination_constructor(destination_expected_values)
                self.assertEqual(
                    dest_field_group.as_dict(destination_expected_instance),
                    dest_field_group.as_dict(destination_instance)
                )

    @patch('a_tuin.metadata.field.Field.use_default')
    def test_update_in_place_field_errors(self, mock_use_default):

        exception_text = 'mock exception'

        def exception_in_use_default(value):
            raise ValueError(exception_text)

        mock_use_default.side_effect = exception_in_use_default

        for (_, source_field_group, source_constructor), (_, dest_field_group, destination_constructor) in \
                inplace_field_group_combinations():

            with self.subTest('{}, {}'.format(type(source_field_group), type(dest_field_group))):

                # need to construct fixtures here as product() shares lists between
                # generated combinations thus test iterations were not independent
                source_instance = source_constructor(INITIAL_VALUES)
                destination_instance = destination_constructor(INITIAL_VALUES)

                mapping = Mapping(source_field_group, dest_field_group)

                with self.assertRaises(FieldErrors) as field_err:
                    mapping.update_in_place(source_instance, destination_instance)

                for fae in field_err.exception._field_errors:
                    self.assertIn(fae.field, source_field_group)
                    self.assertEqual(exception_text, str(fae.original_exception))

    def test_cast_from(self):
        for (_, source_field_group, source_constructor), (_, dest_field_group, destination_constructor) in \
                field_group_combinations():

            with self.subTest('{}, {}'.format(type(source_field_group), type(dest_field_group))):

                source_instance = source_constructor(INITIAL_VALUES)
                mapping = Mapping(source_field_group, dest_field_group)
                destination_instance = mapping.cast_from(source_instance)

                self.assertEqual(
                    EXPECTED_VALUES,
                    dest_field_group.as_dict(destination_instance)
                )

    @patch('a_tuin.metadata.field.Field.type_cast')
    def test_cast_from_field_errors(self, mock_type_cast):
        exception_text = 'mock exception'

        def exception_in_type_cast(value):
            raise ValueError(exception_text)

        mock_type_cast.side_effect = exception_in_type_cast

        for (_, source_field_group, source_constructor), (_, dest_field_group, destination_constructor) in \
                field_group_combinations():

            with self.subTest('{}, {}'.format(type(source_field_group), type(dest_field_group))):

                source_instance = source_constructor(INITIAL_VALUES)
                mapping = Mapping(source_field_group, dest_field_group)
                with self.assertRaises(FieldErrors) as field_err:
                    _ = mapping.cast_from(source_instance)

                for fae in field_err.exception._field_errors:
                    self.assertIn(fae.field, source_field_group)
                    self.assertEqual(exception_text, str(fae.original_exception))

    def test_valid_type_cast(self):
        for (_, source_field_group, source_constructor), (_, dest_field_group, destination_constructor) in \
                field_group_combinations():
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

        expected_instance = EXPECTED_VALUES.copy()
        del expected_instance['name']
        del expected_instance['timestamp']
        self.assertEqual(
            expected_instance,
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

        expected_instance = source_instance.copy()
        expected_instance['dunder'] = '__computed__'
        self.assertEqual(
            expected_instance,
            destination_instance
        )
