__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from unittest import TestCase
from unittest.mock import Mock
from datetime import date

from glod.io.organisation import _parse_inconsistent_birth_date, _parse_phone_numbers


class TestOrganisationBirthDate(TestCase):

    def test_empty(self):
        self.assertEqual(
            None,
            _parse_inconsistent_birth_date('')
        )

    def test_dmY(self):
        self.assertEqual(
            date(2017, 9, 28),
            _parse_inconsistent_birth_date('28/09/2017')
        )

    def test_ymd(self):
        self.assertEqual(
            date(1983, 10, 1),
            _parse_inconsistent_birth_date('831001')
        )

    def test_since_1899(self):
        self.assertEqual(
            date(2003, 9, 8),
            _parse_inconsistent_birth_date('37902')
        )

    def test_too_late(self):
        self.assertEqual(
            None,
            _parse_inconsistent_birth_date('1/1/2090')
        )


def mock_parishioner(phone_number):
    return Mock(telephone=phone_number)


class TestOrganisationPhoneNumbers(TestCase):

    def test_empty(self):
        self.assertEqual(
            (None, None, None),
            _parse_phone_numbers(mock_parishioner(''))
        )

    def test_landline(self):
        self.assertEqual(
            ('298  0092', None, None),
            _parse_phone_numbers(mock_parishioner('298  0092'))
        )

    def test_mobile(self):
        self.assertEqual(
            (None, '083 9389 990', None),
            _parse_phone_numbers(mock_parishioner('083 9389 990'))
        )

    def test_landline_and_mobile(self):
        self.assertEqual(
            ('298  0092', '082 389 2929', None),
            _parse_phone_numbers(mock_parishioner('082 389 2929; 298  0092'))
        )

    def test_two_mobiles(self):
        self.assertEqual(
            (None, '082 389 2929', '088 303 2983'),
            _parse_phone_numbers(mock_parishioner('082 389 2929; 088 303 2983'))
        )

    def test_three_numbers(self):
        self.assertEqual(
            ('698 3893', '082 389 2929', '088 303 2983'),
            _parse_phone_numbers(mock_parishioner('082 389 2929; 698 3893 ; 088 303 2983'))
        )

    def test_excess_numbers(self):
        self.assertEqual(
            ('3839922', '082 389 2929', '088 303 2983'),
            _parse_phone_numbers(mock_parishioner('082 389 2929; 088 303 2983; 3839922; 282018w'))
        )

