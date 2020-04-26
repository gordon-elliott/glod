__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from datetime import datetime, date
from decimal import Decimal
from unittest import TestCase
from unittest.mock import Mock

from a_tuin.metadata.field import (
    StringField,
    IntField,
    FloatField,
    DecimalField,
    DateTimeField,
    DateField,
    ComputedStringField
)


class TestFieldTypeCast(TestCase):

    def setUp(self):
        super().setUp()

        self.fixtures = (
            (StringField, (
                (443, '443'),
                (1.0000002, '1.0000002'),
                (Decimal('100000001.01'), '100000001.01'),
                (datetime(2017, 7, 7, 23, 58, 56), '2017-07-07 23:58:56'),
                (date(2017, 7, 7), '2017-07-07'),
            )),
            (IntField, (
                ('44343', 44343),
                (1.0000002, 1),
                (Decimal('100000001.01'), 100000001),
                (datetime(2017, 7, 7, 23, 58, 56), 736517),
                (date(2017, 7, 7), 736517),
            )),
            (FloatField, (
                ('99999999.000000001', 99999999.000000001),
                (443, 443.0),
                (Decimal('100000001.01'), 100000001.01),
                (datetime(2017, 3, 3, 16, 33, 48, 147333), 1488558828.147333),
                (date(2017, 3, 3), 1488499200.0),
            )),
            (DecimalField, (
                ('345123.99', Decimal('345123.99')),
                (443, Decimal(443)),
                # (1.0000002, Decimal('1.0000002')), TODO match is almost equal
            )),
            (DateTimeField, (
                (1488558823.09768, datetime(2017, 3, 3, 16, 33, 43, 97680)),
                ('2017-07-07 23:58:56', datetime(2017, 7, 7, 23, 58, 56)),
                (736517, datetime(2017, 7, 7)),
                (date(2017, 7, 7), datetime(2017, 7, 7, 0, 0, 0)),
            )),
            (DateField, (
                (1488558823.09768, date(2017, 3, 3)),
                (736517, date(2017, 7, 7)),
                (datetime(2017, 7, 7, 23, 58, 56), date(2017, 7, 7)),
            )),
        )

    def test_type_cast(self):
        for destination_field_type, cast_fixtures in self.fixtures:
            field = destination_field_type('fixture field')
            for input_value, expected in cast_fixtures:
                with self.subTest('Unable to cast {} to {} using {}'.format(input_value, expected, destination_field_type)):
                    self.assertEqual(expected, field.type_cast(input_value), '{}'.format(destination_field_type))

    def test_date_to_string_with_format(self):
        stringfield = StringField('fixture', strfmt='%d/%m/%Y')
        self.assertEqual(
            '30/03/2017',
            stringfield.type_cast(date(2017, 3, 30))
        )


class TestFieldGetValue(TestCase):

    def test_computed(self):
        field_group = Mock()
        computed_field = ComputedStringField(
            'fieldname', lambda field_group, instance: "--{}--".format(instance["attr"])
        )
        self.assertEqual(
            "--Input--",
            computed_field.get_value(field_group, dict(attr="Input"))
        )

    def test_others(self):
        field_group = Mock()
        simple_field_types = (
            StringField,
            IntField,
            FloatField,
            DecimalField,
            DateTimeField,
            DateField,
        )
        for field_type in simple_field_types:
            with self.assertRaises(KeyError):
                field = field_type('field_name')
                field.get_value(field_group, {})


class TestFieldRequired(TestCase):

    def test_required(self):
        field = StringField('fixture', required=True)
        self.assertTrue(field.is_filled('valid'))
        self.assertFalse(field.is_filled(None))

    def test_not_required(self):
        field = StringField('fixture', required=False)
        self.assertTrue(field.is_filled('valid'))
        self.assertTrue(field.is_filled(''))
        self.assertTrue(field.is_filled(None))

    def test_use_default_required(self):
        field = DecimalField('fixture', required=True, default=Decimal('66.66'))
        self.assertEqual(Decimal('0.99'), field.use_default(Decimal('0.99')))
        self.assertEqual(Decimal('66.66'), field.use_default(None))

    def test_use_default_not_required(self):
        field = DecimalField('fixture', required=False, default=Decimal('66.66'))
        self.assertEqual(Decimal('0.99'), field.use_default(Decimal('0.99')))
        self.assertEqual(None, field.use_default(None))
