__copyright__ = 'Copyright(c) Gordon Elliott 2026'
""" Load statements from AIB iBB, Stripe and Sumup via Google Drive
"""
import logging
from datetime import datetime, timezone

#from glod.configuration import configuration
from glod.in_out.account import get_accounts_from_sheet
from glod.in_out.ibb_bank_statement_2026 import StatementLoader
from glod.in_out.statement_item import statement_item_export_files, output_statement_items
from glod.in_out.stripe_bank_statement import load_from_stripe_api
from glod.in_out.sumup_bank_statement import load_from_sumup_api
from glod.model.statement_item import StatementItem
from glod.model.statement_item_collection import StatementItemCollection

LOG = logging.getLogger(__file__)
logging.basicConfig(level=logging.DEBUG)


def do_load(
    configuration,
    sumup_merchant_code, sumup_api_key, sumup_output_spreadsheet, sumup_worksheet,
    stripe_api_key, stripe_output_spreadsheet, stripe_worksheet,
    export_folder, export_file, output_spreadsheet, num_months,
):
    try:
        end_timestamp = datetime.now(tz=timezone.utc)
        load_from_sumup_api(
            sumup_merchant_code, sumup_api_key, sumup_output_spreadsheet, sumup_worksheet, end_timestamp
        )
        load_from_stripe_api(stripe_api_key, stripe_output_spreadsheet, stripe_worksheet)
        _load_from_ibb(configuration, export_file, export_folder, num_months, output_spreadsheet)

    except Exception as ex:
        LOG.exception(ex)
        return 1

    return 0


def _load_from_ibb(configuration, export_file, export_folder, num_months, output_spreadsheet):
    statement_item_exports = list(
        statement_item_export_files(__name__, configuration, configuration.gdrive, export_folder, export_file)
    )

    assert len(statement_item_exports) == 1, "Unexpected number of statement item export files"

    account_collection = get_accounts_from_sheet(configuration)

    loader = StatementLoader(StatementItem, account_collection)

    items = loader.load_from_statement(statement_item_exports[0])
    statement_items = StatementItemCollection(items) \
        .only_most_common_months(num_months) \
        .remove_net_zero_items()

    output_statement_items(
        __name__, configuration, configuration.gdrive, configuration.ledger_sheet, None,
        output_spreadsheet, account_collection, statement_items
    )
