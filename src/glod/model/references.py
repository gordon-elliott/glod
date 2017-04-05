__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.metadata.reference import Reference

from glod.model.account import Account
from glod.model.statement_item import StatementItem
from glod.model.fund import Fund
from glod.model.nominal_account import NominalAccount
from glod.model.subject import Subject


statement_item__account = Reference(StatementItem, 'account', Account)
fund__account = Reference(Fund, 'account', Account)
subject__nominal_account = Reference(Subject, 'nominal_account', NominalAccount)


REFERENCES = (
    statement_item__account,
    fund__account,
    subject__nominal_account,
)
