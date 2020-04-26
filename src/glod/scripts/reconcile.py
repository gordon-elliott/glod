__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" Reconcile transactions to statement items
"""

import logging

from a_tuin.db.session_scope import session_scope
from glod.db.transaction_check import TransactionCheckQuery


LOG = logging.getLogger(__file__)


def reconcile():
    try:
        with session_scope() as session:
            TransactionCheckQuery(session).reconcile()

    except Exception as ex:
        LOG.exception(ex)


if __name__ == '__main__':
    reconcile()
