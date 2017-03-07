__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" Load statement from AIB iBB service
"""


import argparse

from glod.io.ibb_bank_statement import StatementLoader
from glod.io.account import accounts_from_csv
from glod.io.statement_item import statement_item_csv
from glod.model.statement_item import StatementItem
from glod.model.statement_item_collection import StatementItemCollection


def do_load(account_file, export_file, output_csv):
    account_collection = accounts_from_csv(account_file)
    loader = StatementLoader(StatementItem, account_collection)

    items = loader.load_from_statement(export_file)
    collection = StatementItemCollection(items)
    required_items = collection.remove_net_zero_items()
    # TODO restricted to a given month

    with output_csv:
        statement_item_csv(required_items, output_csv)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Load statements extracted from AIB iBB'
    )
    parser.add_argument('account_file', type=argparse.FileType('r'))
    parser.add_argument('export_file', type=argparse.FileType('r'))
    parser.add_argument('out_csv', type=argparse.FileType('w'))
    args = parser.parse_args()

    do_load(args.account_file, args.export_file, args.out_csv)