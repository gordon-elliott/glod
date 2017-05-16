__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.metadata.reference import Reference

from glod.model.account import Account
from glod.model.statement_item import StatementItem
from glod.model.fund import Fund


statement_item__account = Reference(StatementItem, 'account', Account)
fund__account = Reference(Fund, 'account', Account)


REFERENCES = (
    statement_item__account,
    fund__account,
)


def references_from(model_class):
    return (
        reference
        for reference in REFERENCES
        if reference.source_model_class == model_class
    )
