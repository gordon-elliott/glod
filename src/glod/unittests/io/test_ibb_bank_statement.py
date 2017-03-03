__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from decimal import Decimal
from io import StringIO
from unittest import TestCase

from glod.io.ibb_bank_statement import StatementLoader
from glod.io.account import accounts_from_csv
from glod.unittests.io.test_account import ACCOUNT_CSV
from glod.model.statement_item import StatementItem


STATEMENT_FILE = """01,2016-01-10-15.37.55.652000,933554,01638842,CHRIST CHURCH DEL,
02,08/01/2016,,,EUR,,,1263.21,,,1263.21
02,05/01/2016,,,EUR,,,1263.21,,,1263.21
02,04/01/2016,,JOSEPH BLOGGS,EUR,,15.00,1263.21,,,1263.21
02,31/12/2015,,,EUR,,,1248.21,,,1248.21
01,2016-01-10-15.37.55.794000,933554,17559040,CHRISTCHURCH DELGA,
02,08/01/2016,,,EUR,,,684.72,,,684.72
02,04/01/2016,,,EUR,,,684.72,,,684.72
02,31/12/2015,,,EUR,,,684.72,,,684.72
99,End of File"""


class TestStatementLoader(TestCase):

    def test_load_from_statement(self):
        account_collection = accounts_from_csv(StringIO(ACCOUNT_CSV))
        loader = StatementLoader(StatementItem, account_collection)

        items = [
            item for item in loader.load_from_statement(StringIO(STATEMENT_FILE))
        ]

        self.assertEqual(items[2]._details, 'JOSEPH BLOGGS')
        self.assertEqual(
            {'01638842', '17559040'},
            set(stmt._account._account_no for stmt in items)
        )
        self.assertEqual(
            Decimal('15.00'),
            sum(stmt._credit for stmt in items if stmt._credit)
        )

    # TODO account not found
