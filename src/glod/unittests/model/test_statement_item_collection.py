__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from datetime import date, timedelta
from decimal import Decimal
from unittest import TestCase

from glod.model.statement_item import StatementItem
from glod.model.statement_item_collection import StatementItemCollection
from glod.model.account import Account


class TestStatementItemCollection(TestCase):
    
    def setUp(self):
        super().setUp()
        self.account = Account(4003, name='current', account_no='3983789')
        self.one_day = timedelta(1)
        self.today = date.today()

    def test_remove_net_zero_items(self):
        opening_balance = Decimal('1000.00')
        final_credit = Decimal('1.01')
        final_balance = Decimal('1002.02')
        items = (
            # earliest
            StatementItem(self.account, self.today,                    'details', 'EUR', None, Decimal('1.01'), opening_balance),
            StatementItem(self.account, self.today + self.one_day * 1, 'details', 'EUR', Decimal('1.01'), None, Decimal('1001.01')),
            StatementItem(self.account, self.today + self.one_day * 2, 'details', 'EUR', None, None, Decimal('1000.00')),
            StatementItem(self.account, self.today + self.one_day * 3, 'details', 'EUR', None, None, Decimal('1000.00')),
            StatementItem(self.account, self.today + self.one_day * 4, 'details', 'EUR', None, Decimal('1.01'), Decimal('1000.00')),
            StatementItem(self.account, self.today + self.one_day * 5, 'details', 'EUR', None, None, Decimal('1001.01')),
            StatementItem(self.account, self.today + self.one_day * 6, 'details', 'EUR', None, Decimal('1.01'), Decimal('1001.01')),
            StatementItem(self.account, self.today + self.one_day * 7, 'details', 'EUR', None, final_credit, final_balance),
            # latest
        )
        collection = StatementItemCollection(items)
        deduped = list(collection.remove_net_zero_items())

        self.assertEqual(5, len(deduped))
        self.assertEqual(
            final_balance + final_credit,
            opening_balance + sum((item.net for item in deduped))
        )

    def test_remove_net_zero_items_two_accounts(self):
        other_account = Account(4004, name='savings', account_no='9388729')
        opening_balance = Decimal('1000.00')
        items = (
            # earliest
            StatementItem(self.account, self.today,                    'details', 'EUR', None, Decimal('1.01'), opening_balance),
            StatementItem(self.account, self.today + self.one_day * 1, 'details', 'EUR', Decimal('1.01'), None, Decimal('1001.01')),
            StatementItem(self.account, self.today + self.one_day * 2, 'details', 'EUR', None, None, Decimal('1000.00')),
            StatementItem(other_account, self.today + self.one_day * 3, 'details', 'EUR', None, None, Decimal('1000.00')),
            StatementItem(other_account, self.today + self.one_day * 4, 'details', 'EUR', None, Decimal('1.01'), Decimal('1000.00')),
            # latest
        )
        collection = StatementItemCollection(items)
        deduped = list(collection.remove_net_zero_items())

        self.assertEqual(4, len(deduped))

