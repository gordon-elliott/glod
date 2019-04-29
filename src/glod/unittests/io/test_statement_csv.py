
__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from datetime import date
from decimal import Decimal
from io import StringIO
from unittest import TestCase

from glod.model.statement_item import StatementItem
from glod.model.account import Account
from glod.io.statement_item import statement_item_csv


class TestStatementCSV(TestCase):

    def test_export(self):

        account_no = '400400'
        account = Account(8001, 'current', account_no=account_no)
        date_fixture = date.today()
        details = 'details fixture {}'
        currency = 'EUR'
        debit = Decimal('500.00')
        credit = None
        balance = Decimal('3433.22')

        statement_items = [
            StatementItem(
                account,
                date_fixture,
                details.format(i),
                currency,
                debit,
                credit,
                balance,
            )
            for i in range(4)
        ]

        actual = statement_item_csv(statement_items, StringIO()).getvalue()
        expected = """account	date	details	currency	debit	credit	balance\r
{0}	{1}	details fixture 0	{2}	{3}		{4}\r
{0}	{1}	details fixture 1	{2}	{3}		{4}\r
{0}	{1}	details fixture 2	{2}	{3}		{4}\r
{0}	{1}	details fixture 3	{2}	{3}		{4}\r
""".format(
            account_no,
            date_fixture.strftime('%d/%m/%Y'),
            currency,
            debit,
            balance
        )

        self.maxDiff = None
        self.assertEqual(expected, actual)
