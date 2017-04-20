__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from itertools import product

from glod.db.account import Account


def accounts_fixture(statuses, names, institutions, ibans):
    reference = 7000
    for status, name, institution, iban in product(statuses, names, institutions, ibans):
        yield Account(reference, 'purpose', status, name, institution, IBAN=iban)
        reference += 1
