__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""
from datetime import date
from decimal import Decimal

from glod.unittests.db.db_sesssion_test_case import DBSessionTestCase

from glod.db.account import Account, AccountStatus
from glod.db.statement_item import StatementItem

TODAY = date.today()


class TestStatementItem(DBSessionTestCase):

    def test_relationship(self):
        account = Account(7005, 'purpose', AccountStatus.Active, 'current', 'AcmeBank', IBAN='IE49ACME30393002923423223')
        self.session.add(account)
        statement_item = StatementItem(account, TODAY, 'details', 'EUR', Decimal('0.00'), Decimal('30.00'), Decimal('346.65'))
        self.session.add(statement_item)
        self.session.commit()
        ac_id = account.id

        for read_statement in self.session.query(StatementItem):
            self.assertEqual(ac_id, read_statement.account.id)

        new_account = Account(7006, 'purpose', AccountStatus.Active, 'savings', 'AcmeBank', IBAN='IE49ACME39874002923423223')
        self.session.add(new_account)
        self.session.commit()
        new_ac_id = new_account.id

        read_statement.account = new_account

        for reread_statement in self.session.query(StatementItem):
            self.assertEqual(new_ac_id, reread_statement.account.id)

        self.assertEqual(1, len(reread_statement.account.statement_items))