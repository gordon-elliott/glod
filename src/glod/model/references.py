__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.metadata.reference import Reference, REFERENCES

from glod.model.account import Account
from glod.model.statement_item import StatementItem
from glod.model.fund import Fund
from glod.model.counterparty import Counterparty
from glod.model.envelope import Envelope
from glod.model.pps import PPS
from glod.model.subject import Subject
from glod.model.transaction import Transaction
from glod.model.transaction_check import TransactionCheck
from glod.model.address import Address
from glod.model.organisation import Organisation
from glod.model.organisation_address import OrganisationAddress
from glod.model.person import Person
from glod.model.communication_permission import CommunicationPermission


statement_item__account = Reference(StatementItem, 'account', Account)
fund__account = Reference(Fund, 'account', Account)
counterparty__person = Reference(Counterparty, 'person', Person)
counterparty__organisation = Reference(Counterparty, 'organisation', Organisation)
envelope__counterparty = Reference(Envelope, 'counterparty', Counterparty)
envelope__person = Reference(Envelope, 'person', Person)
pps__person = Reference(PPS, 'person', Person)
transaction__counterparty = Reference(Transaction, 'counterparty', Counterparty)
transaction__subject = Reference(Transaction, 'subject', Subject)
transaction__fund = Reference(Transaction, 'fund', Fund)
transaction_check__transaction = Reference(TransactionCheck, 'transaction', Transaction)
transaction_check__statement_item = Reference(TransactionCheck, 'statement_item', StatementItem)
organisation_address__address = Reference(OrganisationAddress, 'address', Address)
organisation_address__organisation = Reference(OrganisationAddress, 'organisation', Organisation)
person__organisation = Reference(Person, 'organisation', Organisation)
communication_permission__person = Reference(CommunicationPermission, 'person', Person)


REFERENCES.extend((
    statement_item__account,
    fund__account,
    counterparty__person,
    counterparty__organisation,
    envelope__counterparty,
    envelope__person,
    pps__person,
    transaction__counterparty,
    transaction__subject,
    transaction__fund,
    transaction_check__transaction,
    transaction_check__statement_item,
    organisation_address__address,
    organisation_address__organisation,
    person__organisation,
    communication_permission__person,
))
