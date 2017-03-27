__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from glod.metadata.reference import Reference

from glod.model.account import Account
from glod.model.statement_item import StatementItem


statement_item__account = Reference(StatementItem, 'account', Account)


REFERENCES = (
    statement_item__account,
)