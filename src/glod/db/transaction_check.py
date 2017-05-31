__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import logging

from sqlalchemy import not_

from glod.db import StatementItemQuery, TransactionQuery, CounterpartyQuery
from glod.model.counterparty import Counterparty
from glod.model.statement_item import StatementItem
from glod.model.transaction import Transaction

from a_tuin.db import TableMap, RelationMap, PagedQuery, InstanceQuery

from glod.model.transaction_check import TransactionCheck, TransactionCheckCollection
from glod.model.references import transaction_check__transaction, transaction_check__statement_item

from glod.db.db_column_type_map import DB_COLUMN_TYPE_MAP

LOG = logging.getLogger(__name__)


TableMap(
    TransactionCheck,
    'transaction_check',
    DB_COLUMN_TYPE_MAP,
    RelationMap(
        transaction_check__transaction,
        'transaction._id',
        backref='checks',
        lazy='joined'
    ),
    RelationMap(
        transaction_check__statement_item,
        'statement_item._id',
        backref='transaction_checks',
        lazy='joined'
    ),
)


class TransactionCheckInstanceQuery(InstanceQuery):
    def __init__(self, session):
        super().__init__(TransactionCheck, TransactionCheckCollection, session)


class TransactionCheckQuery(PagedQuery):
    def __init__(self, session):
        super().__init__(TransactionCheck, TransactionCheckCollection, session)

    def reconcile(self):
        """ Apply rules to transaction and statement items to automatically
            reconcile as many of them as possible. This is not intended to be
            a 100% solution. The function is idempotent; it will only introduce
            TransactionCheck links where none are present.
        """
        not_reconciled_transactions = []
        no_counterparty_found = []
        not_reconciled_statement_items = []

        # manual transactions
        statement_items_by_public_code = StatementItemQuery(self._session) \
            .collection().lookup_map('public_code')

        transactions = TransactionQuery(self._session) \
            .joined_load('checks') \
            .filter(
                Transaction._public_code != None,
                Transaction._public_code != '',
                not_(Transaction.checks.any())
            ) \
            .collection()
        for check in self._model_collection.create_checks(
                transactions,
                statement_items_by_public_code,
                not_reconciled_transactions
        ):
            self._session.add(check)

        # automatic transactions from bank statements
        # associate statement items which have not been reconciled and are without a public_code with a single counter party
        counterparties_by_bank_text = CounterpartyQuery(self._session) \
            .filter(
                Counterparty._bank_text != None,
                Counterparty._bank_text != '',
            ) \
            .collection().lookup_map('bank_text')

        statement_items = StatementItemQuery(self._session) \
            .filter(not_(StatementItem.transaction_checks.any())) \
            .collection().is_null('public_code')

        statement_item_to_counterparty = statement_items.map_to_counterparty(
            counterparties_by_bank_text, no_counterparty_found
        )

        # find the transactions for that counterparty, match on date, amount
        for statement_item, counterparty in statement_item_to_counterparty.items():
            transactions = list(TransactionQuery(self._session)
                .filter(
                    Transaction._counterparty == counterparty,
                    Transaction._amount == statement_item.credit + statement_item.debit,
                    Transaction._year == statement_item.year,
                    Transaction._month == statement_item.month,
                    Transaction._day == statement_item.day,
                    not_(Transaction.checks.any()),
                )
                .collection()
                )

            if transactions:
                assert len(transactions) == 1

                # create check record
                self._session.add(
                    self._model_class(transactions[0], statement_item)
                )
            else:
                # if we can't match on counterparty reference match on counterparty name;
                # some entities have multiple counterparty records, also relax match on exact day
                transactions = list(TransactionQuery(self._session)
                    .filter(
                        Transaction._amount == statement_item.credit + statement_item.debit,
                        Transaction._year == statement_item.year,
                        Transaction._month == statement_item.month,
                        not_(Transaction.checks.any()),
                    )
                    .collection()
                    .filter(lambda t: t.counterparty.lookup_name == counterparty.lookup_name)
                )

                if transactions:
                    assert len(transactions) == 1

                    transaction = transactions[0]
                    # update transaction to refer to correct counterparty
                    transaction.counterparty = counterparty
                    # create check record
                    self._session.add(
                        self._model_class(transaction, statement_item)
                    )
                else:
                    not_reconciled_statement_items.append(statement_item)

        if not_reconciled_transactions:
            not_reconciled_transactions.sort(key=lambda t: t.reference_no)
            LOG.warning('Unable to reconcile {} transactions:\n{}'.format(
                len(not_reconciled_transactions), '\n'.join(map(str, not_reconciled_transactions))
            ))
        if no_counterparty_found:
            LOG.warning('Unable find counterparty for {} statement items:\n{}'.format(
                len(no_counterparty_found), '\n'.join(map(str, no_counterparty_found))
            ))
        if not_reconciled_statement_items:
            not_reconciled_statement_items.sort(key=lambda si: si.trimmed_details)
            LOG.warning('Unable to reconcile {} statement items:\n{}'.format(
                len(not_reconciled_statement_items), '\n'.join(map(str, not_reconciled_statement_items))
            ))
