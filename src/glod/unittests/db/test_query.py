__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""
from collections import OrderedDict

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

    def test_paging_first(self):
        self._load_fixtures()

        accounts = self.account_query.limit(3).collection()
        ref_nos = tuple(account.reference_no for account in accounts)

        self.assertEqual((7000, 7001, 7002), ref_nos)
        self.assertEqual(0, self.account_query.start_index)
        self.assertEqual(2, self.account_query.end_index)

    def test_paging_middle(self):
        self._load_fixtures()

        accounts = self.account_query.offset(2).limit(3).collection()
        ref_nos = tuple(account.reference_no for account in accounts)

        self.assertEqual((7003, 7004, 7005), ref_nos)
        self.assertEqual(3, self.account_query.start_index)
        self.assertEqual(5, self.account_query.end_index)

    def test_paging_last(self):
        self._load_fixtures()

        accounts = self.account_query.offset(5).limit(3).collection()
        ref_nos = tuple(account.reference_no for account in accounts)

        self.assertEqual((7006, 7007), ref_nos)
        self.assertEqual(6, self.account_query.start_index)
        self.assertEqual(7, self.account_query.end_index)

    def test_sort(self):
        self._load_fixtures()

        sort_criteria = tuple(self.account_query.sort_criteria_from_dict({'_reference_no': False}))
        accounts = self.account_query.order_by(*sort_criteria).collection()
        ref_nos = tuple(account.reference_no for account in accounts)

        self.assertEqual((7007, 7006, 7005, 7004, 7003, 7002, 7001, 7000), ref_nos)

    def test_sort_multiple_criteria(self):
        self._load_fixtures()

        sort_criteria = tuple(self.account_query.sort_criteria_from_dict(
            OrderedDict((('_name', True), ('_reference_no', False)))
        ))
        accounts = self.account_query.order_by(*sort_criteria).collection()
        ref_nos = tuple((account.name, account.reference_no) for account in accounts)

        self.assertEqual(
            tuple(zip(
                ('current',) * 4 + ('savings',) * 4,
                (7005, 7004, 7001, 7000, 7007, 7006, 7003, 7002),
            )),
            ref_nos
        )
        self.assertEqual(0, self.account_query.start_index)
        self.assertEqual(7, self.account_query.end_index)

    def test_sort_paging(self):
        self._load_fixtures()

        sort_criteria = tuple(self.account_query.sort_criteria_from_dict({'_reference_no': False}))
        accounts = self.account_query.order_by(*sort_criteria).offset(2).limit(3).collection()
        ref_nos = tuple(account.reference_no for account in accounts)

        self.assertEqual((7004, 7003, 7002), ref_nos)
        self.assertEqual(3, self.account_query.start_index)
        self.assertEqual(5, self.account_query.end_index)
