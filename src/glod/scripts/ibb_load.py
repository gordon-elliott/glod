__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" Load statement from AIB iBB service
"""


import argparse
import logging
import sys

from glod.in_out.ibb_bank_statement import StatementLoader
from glod.in_out.statement_item import output_statement_items
from glod.in_out.account import get_account_collection
from glod.db.statement_item import StatementItem, StatementItemCollection


LOG = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)


def do_load(account_file, export_file, output_csv, output_spreadsheet, output_worksheet, num_months):
    try:
        account_collection = get_account_collection(account_file)

        loader = StatementLoader(StatementItem, account_collection)

        items = loader.load_from_statement(export_file)
        statement_items = StatementItemCollection(items) \
            .only_most_common_months(num_months) \
            .remove_net_zero_items()

        output_statement_items(output_csv, output_spreadsheet, output_worksheet, statement_items)

    except Exception as ex:
        LOG.exception(ex)
        return 1

    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Load statements extracted from AIB iBB'
    )
    parser.add_argument('export_file', type=argparse.FileType('r'))
    parser.add_argument('--account_file', type=argparse.FileType('r'), required=False)
    parser.add_argument('--out_csv', type=argparse.FileType('w'), required=False)
    parser.add_argument('--out_spreadsheet', type=str, required=False)
    parser.add_argument('--out_worksheet', type=str, required=False, default='statement items')
    parser.add_argument('--num_months', type=int, required=False, default=1)
    args = parser.parse_args()

    sys.exit(do_load(
        args.account_file, args.export_file, args.out_csv,
        args.out_spreadsheet, args.out_worksheet, args.num_months
    ))
