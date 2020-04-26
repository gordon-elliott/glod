__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.metadata import (
    ObjectFieldGroupBase,
    ObjectReferenceField,
    Collection,
)


class TransactionCheck(ObjectFieldGroupBase):

    public_interface = (
        ObjectReferenceField('transaction'),
        ObjectReferenceField('statement_item'),
    )


class TransactionCheckCollection(Collection):

    @classmethod
    def create_checks(cls, transactions, statement_items_by_public_code, not_reconciled_transactions):
        # find transactions with public_codes and without reconciliation items
        # find the public_code in the statement_item description
        # create a reconciliation instance to link them
        for transaction in transactions:
            public_code = transaction.public_code
            if public_code in statement_items_by_public_code:
                yield TransactionCheck(transaction, statement_items_by_public_code[public_code])
            else:
                not_reconciled_transactions.append(transaction)
