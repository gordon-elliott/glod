__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

from decimal import Decimal

from glod.model.collection import Collection


# TODO sequence no

class StatementItemCollection(Collection):

    def remove_net_zero_items(self):

        last_item = None
        for item in self._items:
            is_different_account = last_item is None or last_item._account != item._account
            if is_different_account or item.net != Decimal('0.00'):
                yield item
            last_item = item
