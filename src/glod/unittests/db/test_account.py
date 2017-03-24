__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from glod.unittests.db.db_sesssion_test_case import DBSessionTestCase

from glod.db.account import Account


class TestAccount(DBSessionTestCase):

    def test_table_exists(self):
        no_accounts = self.session.query(Account)

        self.assertEqual([], list(no_accounts))

    def test_crud(self):

        institution = 'AcmeBank'
        account = Account('purpose', 'active', 'current', institution, IBAN='IE49ACME30393002923423223')
        self.session.add(account)
        self.session.commit()
        ac_id = account.id

        num_accounts = 0
        for read_account in self.session.query(Account):
            self.assertEqual(ac_id, read_account.id)
            self.assertEqual(institution, read_account.institution)
            num_accounts += 1

        self.assertEqual(1, num_accounts)

        new_status = 'closed'
        read_account.status = new_status
        self.session.commit()

        for updated_account in self.session.query(Account):
            self.assertEqual(new_status, updated_account.status)

            self.session.delete(updated_account)

        self.session.commit()

        no_accounts = self.session.query(Account)
        self.assertEqual([], list(no_accounts))
