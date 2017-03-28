__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from glod.unittests.db.db_sesssion_test_case import DBSessionTestCase
from glod.unittests.db.fixtures import accounts_fixture

from glod.db.account import Account, AccountStatus, AccountQuery


class TestQuery(DBSessionTestCase):

    def setUp(self):
        super().setUp()

        self.accounts = accounts_fixture(
            (AccountStatus.Active, AccountStatus.Closed),
            ('current', 'savings'),
            ('BigBank', 'TooBigBank'),
            ('IE88BBNK3938320298229',)
        )
        self.account_query = AccountQuery(self.session)

    def tearDown(self):
        super().tearDown()

        self.session.query(Account).delete()
        self.session.commit()

    def _load_fixtures(self):
        for account in self.accounts:
            self.session.add(account)
        self.session.commit()

    def test_empty_table(self):
        self.assertEqual(0, len(self.account_query))

    def test_no_results_match(self):
        self._load_fixtures()

        accounts = self.account_query.filter(Account.c._IBAN == 'nomatch')

        self.assertEqual(0, len(accounts))

    def test_all(self):
        self._load_fixtures()

        self.assertEqual(8, len(self.account_query))
        self.assertEqual(8, len(list(self.account_query)))

    def test_one_match(self):
        self._load_fixtures()

        status = AccountStatus.Active
        name = 'savings'
        institution = 'TooBigBank'

        accounts = self.account_query.filter(
            Account.c._status == status,
            Account.c._name == name,
            Account.c._institution == institution
        )

        self.assertEqual(1, len(accounts))
        account = list(accounts)[0]
        self.assertEqual(status, account.status)
        self.assertEqual(name, account.name)
        self.assertEqual(institution, account.institution)

    def test_paging(self):
        self._load_fixtures()

        accounts = self.account_query.offset(2).limit(3)

        self.assertEqual(3, len(accounts))
