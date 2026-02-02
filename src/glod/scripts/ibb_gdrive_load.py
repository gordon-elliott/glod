__copyright__ = 'Copyright(c) Gordon Elliott 2020'
""" Load statement from AIB iBB service via Google Drive
"""


import argparse
import logging
import sys

from glod.configuration import configuration
from glod.in_out.account import get_account_collection
from glod.in_out.ibb_bank_statement import StatementLoader
from glod.in_out.statement_item import statement_item_export_files, output_statement_items
from glod.model.statement_item import StatementItem
from glod.model.statement_item_collection import StatementItemCollection

LOG = logging.getLogger(__file__)
logging.basicConfig(level=logging.DEBUG)


def do_load(account_filename, export_folder, export_file, output_spreadsheet, num_months):
    try:
        with open(account_filename) as account_file:
            account_collection = get_account_collection(account_file)

        loader = StatementLoader(StatementItem, account_collection)

        statement_item_exports = list(
            statement_item_export_files(__name__, configuration, configuration.gdrive, export_folder, export_file)
        )

        assert len(statement_item_exports) == 1, "Unexpected number of statement item export files"

        items = loader.load_from_statement(statement_item_exports[0])
        statement_items = StatementItemCollection(items) \
            .only_most_common_months(num_months) \
            .remove_net_zero_items()

        output_statement_items(__name__, configuration, configuration.gdrive, configuration.ledger_sheet, None,
            output_spreadsheet, account_collection, statement_items)

    except Exception as ex:
        LOG.exception(ex)
        return 1

    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Load statements extracted from AIB iBB'
    )
    parser.add_argument('export_folder', type=str)
    parser.add_argument('export_file', type=str)
    parser.add_argument('out_spreadsheet', type=str)
    parser.add_argument('--account_file', type=str, required=False)
    parser.add_argument('--num_months', type=int, required=False, default=1)
    args = parser.parse_args()

    sys.exit(do_load(
        args.account_file, args.export_folder, args.export_file,
        args.out_spreadsheet, args.num_months
    ))
