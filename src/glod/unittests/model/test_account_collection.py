__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

from unittest import TestCase

from glod.model.account import Account, AccountStatus, AccountCollection


class TestAccountCollection(TestCase):

    def test_lookup(self):

        account_list_fixture = [
            Account(7000+i, 'purpose', AccountStatus.Active, 'name', 'institution', 'sort code', 'account_{}'.format(i), 'bic', 'iban')
            for i in range(5)
        ]
        account_collection = AccountCollection(
            account_list_fixture
        )

        self.assertEqual(
            account_list_fixture[3],
            list(account_collection.lookup('account_3', '_account_no'))[0]
        )
