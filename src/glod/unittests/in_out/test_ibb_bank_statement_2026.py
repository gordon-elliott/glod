__copyright__ = 'Copyright(c) Gordon Elliott 2026'

""" 
"""

from decimal import Decimal
from io import StringIO
from unittest import TestCase

from glod.in_out.account import accounts_from_csv
from glod.in_out.ibb_bank_statement_2026 import StatementLoader
from glod.model.statement_item import StatementItem
from glod.unittests.in_out.test_account import ACCOUNT_CSV

STATEMENT_FILE = """"Account / IBAN","Pending (P) / Historical (H)","Amount","Currency","Credit / Debit","Date","Transaction Narrative","Balance","Balance Credit / Debit","Transaction Reference","Creditor Name","Debtor Name"
"IE66AIBK93355401638172","H","150.00","EUR","Credit","2025-01-02","HEATING TOKENS",,,"IE25010242969049","CHRIST CHURCH DELG","MIRANDA ASHTON & THERESE LEDDY"
"IE66AIBK93355401638172","H","500.00","EUR","Credit","2025-01-02","33642EARLYBIRDS","20806.96","Credit","IE25010242968807","CHRIST CHURCH DELG","MIRANDA ASHTON & THERESE LEDDY"
"IE66AIBK93355401638172","H","50.00","EUR","Credit","2025-01-03","E17814",,,"IE25010344822936","CCD OLD SCHOOL HOU","CHRIST CHURCH DELGANY"
"IE66AIBK93355401638172","H","-120.00","EUR","Debit","2025-01-03","D17812","20736.96","Credit","IE25010344822893","CHRIST CHURCH DGNY","CHRIST CHURCH DELGANY"
"IE66AIBK93355401638172","H","275.00","EUR","Credit","2025-01-06","*ATMLDG G'STONES A L17826",,,,,
"IE66AIBK93355401638172","H","-1.00","EUR","Debit","2025-03-31","GOVSTMPDTY01638172 2@ 0.50 EACH","19232.02","Credit",,,
"IE18AIBK93355401638842","H","-0.50","EUR","Debit","2024-12-31","GOVSTMPDTY11871169 1@ 0.50 EACH","975.03","Credit",,,
"IE18AIBK93355401638842","H","500.00","EUR","Credit","2025-01-03","E17810","1475.03","Credit","IE25010344822943","CANON NIGEL WAUGH","CHRIST CHURCH DELGANY"
"IE18AIBK93355401638842","H","-2.44","EUR","Debit","2025-03-28","FEE-QTR TO 28FEB25 933554-11871169","1472.59","Credit",,,
"""


class TestStatementLoader(TestCase):

    def test_load_from_statement(self):
        account_collection = accounts_from_csv(StringIO(ACCOUNT_CSV))
        loader = StatementLoader(StatementItem, account_collection)

        items = [
            item for item in loader.load_from_statement(StringIO(STATEMENT_FILE))
        ]

        self.assertEqual(items[6]._details, 'E17814')
        self.assertEqual(
            {'01638842', '01638172'},
            set(stmt._account._account_no for stmt in items)
        )
        self.assertEqual(
            Decimal('1475.00'),
            sum(stmt._credit for stmt in items if stmt._credit)
        )
        self.assertEqual(
            Decimal('120.00'),
            items[5]._debit
        )
