__copyright__ = 'Copyright(c) Gordon Elliott 2020'
""" 
"""

import logging

from functools import partial
from csv import DictWriter, excel_tab
from datetime import date, datetime

from a_tuin.metadata import StringField, TransformedStringField, DictFieldGroup, Mapping, TupleFieldGroup
from a_tuin.db.session_scope import session_scope
from a_tuin.in_out.google_drive import get_gdrive_service, files_in_folder, download, get_credentials_path
from a_tuin.in_out.google_sheets import configure_client
from a_tuin.in_out.gsheet_integration import get_gsheet_fields, load_class

from glod.configuration import configuration
from glod.in_out.casts import strip_commas
from glod.db.statement_item import StatementItem, StatementItemDesignatedBalance
from glod.db.account import AccountQuery

LOG = logging.getLogger(__name__)


def _statement_item_export_fields():
    field_names = tuple(
        field.name
        for field in StatementItem.constructor_parameters
    )

    def extract_account_no(account):
        return account._account_no

    csv_fields = tuple(
        TransformedStringField(name, extract_account_no) if name == 'account' else StringField(name)
        for name in field_names
        if name not in ('detail_override', 'designated_balance')
    )
    csv_fields[1]._strfmt = '%d/%m/%Y'
    return csv_fields


def statement_item_csv(statement_items, csv_file):

    csv_fields = _statement_item_export_fields()
    csv_field_names = [field.name for field in csv_fields]
    csv_field_group = DictFieldGroup(csv_fields)

    internal_to_csv = Mapping(StatementItem.internal, csv_field_group)

    csv_writer = DictWriter(csv_file, csv_field_names, dialect=excel_tab)
    csv_writer.writeheader()

    for statement_item in statement_items:
        csv_writer.writerow(
            internal_to_csv.cast_from(statement_item)
        )

    return csv_file


def ignore_na(value, _):
    if value == 'N/A':
        return None
    else:
        return strip_commas(value, _)


def cast_dmy_date_from_string(value, _):
    return date.fromtimestamp(datetime.strptime(value, '%d/%m/%Y').timestamp())


def cast_designated_balance(value, _):
    if not value:
        return StatementItemDesignatedBalance.No
    elif value.lower() == 'opening':
        return StatementItemDesignatedBalance.Opening
    else:
        return StatementItemDesignatedBalance.Closing


def statement_item_from_gsheet(session, extract_from_detailed_ledger):

    statement_item_gsheet = get_gsheet_fields(StatementItem, None)
    field_casts = {
        'account': AccountQuery(session).instance_finder('account_no', None),
        'date': cast_dmy_date_from_string,
        'debit': strip_commas,
        'credit': strip_commas,
        'balance': ignore_na,
        'designated balance': cast_designated_balance,
    }
    statement_item_mapping = Mapping(statement_item_gsheet, StatementItem.constructor_parameters, field_casts=field_casts)
    statement_items = extract_from_detailed_ledger(
        'bank statements',
        'A1',
        ('account', 'date', 'details', 'currency', 'debit', 'credit', 'balance', 'detail override', 'designated balance')
    )
    load_class(session, statement_items, statement_item_mapping, StatementItem)


def _append(statement_items, worksheet):
    gsheet_field_names, statement_items_for_gsheet = _statement_items_for_gsheet(statement_items)
    worksheet.append_rows(
        [gsheet_field_names] + list(statement_items_for_gsheet)
    )


def _statement_items_for_gsheet(statement_items):
    gsheet_fields = _statement_item_export_fields()
    gsheet_field_names = [field.name for field in gsheet_fields]
    gsheet_field_group = TupleFieldGroup(gsheet_fields)
    internal_to_gsheet = Mapping(StatementItem.internal, gsheet_field_group)
    statement_items_for_gsheet = (
        internal_to_gsheet.cast_from(statement_item)
        for statement_item in statement_items
    )
    return gsheet_field_names, statement_items_for_gsheet


def statement_item_export_files(module_name, drive_config, fy, sequence_no):
    service = get_gdrive_service(module_name, drive_config)
    walk_folder = partial(files_in_folder, service)

    for statements_folder_id, _ in walk_folder(f"sharedWithMe and name = '{drive_config.account_statements_folder}'"):
        for fy_folder_id, _ in walk_folder(f"'{statements_folder_id}' in parents and name = '{fy}'"):
            for statement_file_id, statement_filename in walk_folder(f"'{fy_folder_id}' in parents and name contains '({sequence_no})'"):
                LOG.info(f"Loading statement items from {fy}/{statement_filename} ({statement_file_id})")
                request = service.files().get_media(fileId=statement_file_id)
                yield download(request)


def _new_sheet(module_name, drive_config, output_spreadsheet_name):
    credentials_path = get_credentials_path(module_name, configuration.google_sheets)
    google_sheets_client = configure_client(credentials_path)
    si_sheet = google_sheets_client.create(output_spreadsheet_name)
    # TODO: get collaborators from config
    si_sheet.share('gordon.e.elliott@gmail.com', perm_type='user', role='writer')
    worksheet = si_sheet.sheet1
    worksheet.update_title(drive_config.statement_items_sheet_name)
    worksheet.freeze(rows=1)
    worksheet.format("A", {'numberFormat': {'type': 'TEXT'}})   # TODO: perhaps strip leading 0
    worksheet.format("B", {'numberFormat': {'type': 'DATE', 'pattern': 'dd/mm/yyy'}, 'horizontalAlignment': 'RIGHT'})
    worksheet.format("C:D", {'numberFormat': {'type': 'TEXT'}})
    worksheet.format("E:G", {'numberFormat': {'type': 'NUMBER', 'pattern': '#,###.00'}, 'horizontalAlignment': 'RIGHT'})
    return si_sheet, worksheet


def open_sheet(module_name, drive_config, output_spreadsheet):
    credentials_path = get_credentials_path(module_name, drive_config)
    google_sheets_client = configure_client(credentials_path)
    import gspread
    try:
        return google_sheets_client.open_by_key(output_spreadsheet)
    except gspread.SpreadsheetNotFound:
        # TODO: get check for non-existent ss working
        return None


def _merge(statement_items, worksheet, account_collection):
    for account in account_collection:
        first_account_cell = worksheet.find(account._account_no)
        _, statement_items_for_gsheet = _statement_items_for_gsheet(statement_items)
        # TODO filter statement items by account
        row_before = first_account_cell.row - 1
        LOG.info(f"Inserting after row {row_before}")
        worksheet.append_rows(
            list(statement_items_for_gsheet),
            insert_data_option='INSERT_ROWS',
            table_range=f"A{row_before}"
        )
        # bug - no rows being added


def output_statement_items(
        module_name,
        drive_config,
        output_csv,
        output_spreadsheet,
        output_worksheet,
        account_collection,
        statement_items
):
    if output_spreadsheet:
        gsheet = open_sheet(module_name, drive_config, output_spreadsheet)
        if gsheet:
            import gspread
            try:
                worksheet = gsheet.worksheet(drive_config.statement_items_sheet_name)
            except gspread.exceptions.WorksheetNotFound:
                worksheet = None
            if worksheet:
                worksheet.duplicate(new_sheet_name=output_worksheet)
            else:
                worksheet = gsheet.add_worksheet(title=drive_config.statement_items_sheet_name)
            LOG.info(f"Merging with existing gsheet {output_spreadsheet}")
            _merge(statement_items, worksheet, account_collection)
        else:
            _, worksheet = _new_sheet(module_name, drive_config, output_spreadsheet)
            LOG.info(f"Writing to new gsheet {output_spreadsheet}")
            _append(statement_items, worksheet)
    elif output_csv:
        with output_csv:
            statement_item_csv(statement_items, output_csv)
    else:
        with session_scope() as session:
            for statement_item in statement_items:
                session.add(statement_item)