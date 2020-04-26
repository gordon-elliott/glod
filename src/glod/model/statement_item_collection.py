__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

from collections import defaultdict
from decimal import Decimal
from operator import itemgetter

from a_tuin.metadata import Collection, chainable


# TODO sequence no


class StatementItemCollection(Collection):

    @chainable
    def remove_net_zero_items(self, items):

        last_item = None
        items_per_account = 0
        account_balance_item = None

        for item in items:
            is_different_account = last_item is None or last_item._account != item._account
            if is_different_account:
                # if we've gone onto the next account and no non-zero items were yielded
                # from the last account yield an item which just reports the account balance
                if account_balance_item and items_per_account == 0:
                    yield account_balance_item
                items_per_account = 0
                account_balance_item = None
            if item.net == Decimal('0.00'):
                account_balance_item = item
            else:
                items_per_account += 1
                yield item
            last_item = item

        if account_balance_item and items_per_account == 0:
            yield account_balance_item


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

    def map_to_counterparty(self, counterparties_by_bank_text, no_counterparty_found):
        statement_item_to_counterparty = {}
        for statement_item in self:
            details = statement_item.trimmed_details

            if details in counterparties_by_bank_text:
                statement_item_to_counterparty[statement_item] = counterparties_by_bank_text[details]
            else:
                matched = False
                for bank_text, counterparty in counterparties_by_bank_text.items():
                    if details.startswith(bank_text):
                        statement_item_to_counterparty[statement_item] = counterparty
                        matched = True
                        break

                if not matched:
                    no_counterparty_found.append(statement_item)

        return statement_item_to_counterparty
