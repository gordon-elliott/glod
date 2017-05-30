__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.metadata.reference import Reference

from glod.model.account import Account
from glod.model.statement_item import StatementItem
from glod.model.fund import Fund
from glod.model.counterparty import Counterparty
from glod.model.parishioner import Parishioner
from glod.model.envelope import Envelope
from glod.model.pps import PPS
from glod.model.subject import Subject
from glod.model.transaction import Transaction
from glod.model.transaction_check import TransactionCheck


statement_item__account = Reference(StatementItem, 'account', Account)
fund__account = Reference(Fund, 'account', Account)
counterparty__parishioner = Reference(Counterparty, 'parishioner', Parishioner)
envelope__counterparty = Reference(Envelope, 'counterparty', Counterparty)
envelope__parishioner = Reference(Envelope, 'parishioner', Parishioner)
pps__parishioner = Reference(PPS, 'parishioner', Parishioner)
transaction__counterparty = Reference(Transaction, 'counterparty', Counterparty)
transaction__subject = Reference(Transaction, 'subject', Subject)
transaction__fund = Reference(Transaction, 'fund', Fund)
transaction_check__transaction = Reference(TransactionCheck, 'transaction', Transaction)
transaction_check__statement_item = Reference(TransactionCheck, 'statement_item', StatementItem)


REFERENCES = (
    statement_item__account,
    fund__account,
    counterparty__parishioner,
    envelope__counterparty,
    envelope__parishioner,
    pps__parishioner,
    transaction__counterparty,
    transaction__subject,
    transaction__fund,
    transaction_check__transaction,
    transaction_check__statement_item,
)


def references_from(model_class):
    return (
        reference
        for reference in REFERENCES
        if reference.source_model_class == model_class
    )
