__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

from collections import defaultdict
from decimal import Decimal
from operator import itemgetter

from glod.model.collection import Collection, chainable


# TODO sequence no


class StatementItemCollection(Collection):

    @chainable
    def remove_net_zero_items(self, items):

        last_item = None
        for item in items:
            is_different_account = last_item is None or last_item._account != item._account
            if is_different_account or item.net != Decimal('0.00'):
                yield item
            last_item = item

    @chainable
    def only_most_common_months(self, items, num_months):

        item_list = list(items)
        month_counts = defaultdict(int)
        for item in item_list:
            month_counts[item.month] += 1

        months_in_order = sorted(month_counts.items(), key=itemgetter(1), reverse=True)
        desired_months = set(map(itemgetter(0), months_in_order[:num_months]))

        for item in item_list:
            if item.month in desired_months:
                yield item
