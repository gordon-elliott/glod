__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

from io import StringIO
from unittest import TestCase

from glod.in_out.account import accounts_from_csv


ACCOUNT_CSV = """id,purpose,status,name,institution,sort code,account no,BIC,IBAN,display name,units
7001,current,in use,CHRIST CHURCH DGNY,AIB,933554,01638172,AIBKIE2D,IE66 AIBK 9335 5401 6381 72,current (1638172),
7003,mission committee,in use,CHRIST CHURCH DEL,AIB,933554,01638842,AIBKIE2D,IE18 AIBK 9335 5401 6388 42,mission committee (1638842),
7004,savings,ready,CHRISTCHURCH DELGA,AIB,933554,17559040,AIBKIE2D,IE84 AIBK 9335 5417 5590 40,savings (17559040),"""


class TestAccount(TestCase):

    def test_load(self):
        collection = accounts_from_csv(StringIO(ACCOUNT_CSV))

        self.assertEqual(3, len(list(collection)))
        item3 = list(collection.lookup('01638842', '_account_no'))[0]
        self.assertEqual('mission committee', item3._purpose)

