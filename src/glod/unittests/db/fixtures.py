from itertools import product

from glod.model.account import Account

__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""


def accounts_fixture(statuses, names, institutions, ibans):
    for status, name, institution, iban in product(statuses, names, institutions, ibans):
        yield Account('purpose', status, name, institution, IBAN=iban)