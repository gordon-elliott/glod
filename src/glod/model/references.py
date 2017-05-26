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


statement_item__account = Reference(StatementItem, 'account', Account)
fund__account = Reference(Fund, 'account', Account)
counterparty__parishioner = Reference(Counterparty, 'parishioner', Parishioner)
envelope__counterparty = Reference(Envelope, 'counterparty', Counterparty)
envelope__parishioner = Reference(Envelope, 'parishioner', Parishioner)
pps__parishioner = Reference(PPS, 'parishioner', Parishioner)


REFERENCES = (
    statement_item__account,
    fund__account,
    counterparty__parishioner,
    envelope__counterparty,
    envelope__parishioner,
    pps__parishioner,
)


def references_from(model_class):
    return (
        reference
        for reference in REFERENCES
        if reference.source_model_class == model_class
    )
