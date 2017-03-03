__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

from io import StringIO
from unittest import TestCase

from glod.io.account import accounts_from_csv


ACCOUNT_CSV = """id,purpose,status,name,institution,sort code,account no,BIC,IBAN,display name,units
7001,current,in use,CHRIST CHURCH DGNY,AIB,933554,01638172,AIBKIE2D,IE66 AIBK 9335 5401 6381 72,current (1638172),
7002,building,ready,CHRIST CHURCH BLD,AIB,933554,01638339,AIBKIE2D,IE19 AIBK 9335 5401 6383 39,building (1638339),
7003,mission committee,in use,CHRIST CHURCH DEL,AIB,933554,01638842,AIBKIE2D,IE18 AIBK 9335 5401 6388 42,mission committee (1638842),
7004,savings,ready,CHRISTCHURCH DELGA,AIB,933554,17559040,AIBKIE2D,IE84 AIBK 9335 5417 5590 40,savings (17559040),
7005,deposit - term,closed,CHRIST CHURCH DEL,AIB,933554,17559123,AIBKIE2D,IE74 AIBK 9335 5417 5591 23,deposit - term (17559123),
7006,deposit - term,in use,12 Month Fixed,KBC,990270,10601993,ICONIE2D,IE78 9902 7010 6019 93,deposit - term (10601993),
7007,deposit - demand,in use,Smart Demand,KBC,990270,10528926,ICONIE2D,IE78 9902 7010 5289 26,deposit - demand (10528926),
7008,osh,in use,CCD Old School House,AIB,933554,10253021,AIBKIE2D,IE02 AIBK 9335 5410 2530 21,osh (10253021),
7009,social committee,closed,Social Committtee,AIB,933554,12675007,AIBKIE2D,IE02 AIBK 9335 5412 6750 07,social committee (12675007),
7010,unit trust,in use,R.B. General Unit Trust,RCB,,CCD,,,unit trust (CCD),204.49
7011,discretionary fund,in use,CANON NIGEL WAUGH FRIENDLY FUND   ,AIB,933554,11871169,AIBKIE2D,IE67 AIBK 9335 5411 8711 69,discretionary fund (11871169),"""


class TestAccount(TestCase):

    def test_load(self):
        collection = accounts_from_csv(StringIO(ACCOUNT_CSV))

        self.assertEqual(11, len(collection))
        item3 = list(collection.lookup(7004, '_id'))[0]
        self.assertEqual('17559040', item3._account_no)

