__copyright__ = 'Copyright(c) Gordon Elliott 2020'
""" 
"""

import logging

from functools import partial
from csv import DictWriter, excel_tab

from a_tuin.metadata import StringField, TransformedStringField, DictFieldGroup, Mapping, TupleFieldGroup, FloatField
from a_tuin.db.session_scope import session_scope
from a_tuin.in_out.google_drive import get_gdrive_service, files_in_folder, download_textfile, get_credentials_path
from a_tuin.in_out.google_sheets import configure_client, insert_rows, open_sheet
from a_tuin.in_out.gsheet_integration import get_gsheet_fields, load_class

from glod.in_out.casts import strip_commas, cast_dmy_date_from_string
from glod.in_out.account import get_accounts_from_sheet
from glod.in_out.ibb_bank_statement import StatementLoader
from glod.model.statement_item_collection import StatementItemCollection
from glod.db.statement_item import StatementItem, StatementItemDesignatedBalance
from glod.db.account import AccountQuery

LOG = logging.getLogger(__name__)
COMPUTED_FIELDS = ('detail_override', 'designated_balance')


def _extract_account_no(account):
    return account._account_no


def _statement_item_export_fields():
    field_names = tuple(
        field.name
        for field in StatementItem.constructor_parameters
    )
    csv_fields = tuple(
        TransformedStringField(name, _extract_account_no) if name == 'account' else StringField(name)
        for name in field_names
        if name not in COMPUTED_FIELDS
    )
    csv_fields[1]._strfmt = '%d/%m/%Y'
    return csv_fields


def _statement_item_gsheet_export_fields():
    transformed_fields_map = {
        'account': TransformedStringField('account', _extract_account_no),
        'date': StringField('date', strfmt='%d/%m/%Y'),
        'debit': FloatField('debit'),
        'credit': FloatField('credit'),
        'balance': FloatField('balance'),
    }
    gsheet_fields = tuple(
        transformed_fields_map.get(field.name, field)
        for field in StatementItem.public_interface
        if field.name not in COMPUTED_FIELDS
    )
    return gsheet_fields


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
    gsheet_fields = _statement_item_gsheet_export_fields()
    gsheet_field_names = [field.name for field in gsheet_fields]
    gsheet_field_group = TupleFieldGroup(gsheet_fields)
    internal_to_gsheet = Mapping(StatementItem.internal, gsheet_field_group)
    statement_items_for_gsheet = (
        internal_to_gsheet.cast_from(statement_item)
        for statement_item in statement_items
    )
    return gsheet_field_names, statement_items_for_gsheet


def statement_item_export_files(module_name, drive_config, fy, sequence_no):
    from glod.configuration import configuration
    service = get_gdrive_service(configuration)
    walk_folder = partial(files_in_folder, service)

    for statements_folder_id, _ in walk_folder(f"sharedWithMe and name = '{drive_config.account_statements_folder}'"):
        for fy_folder_id, _ in walk_folder(f"'{statements_folder_id}' in parents and name = '{fy}'"):
            for statement_file_id, statement_filename in walk_folder(f"'{fy_folder_id}' in parents and name contains '({sequence_no})'"):
                LOG.info(f"Loading statement items from {fy}/{statement_filename} ({statement_file_id})")
                request = service.files().get_media(fileId=statement_file_id)
                yield download_textfile(request)


def _new_sheet(module_name, drive_config, ledger_config, output_spreadsheet_name):
    from glod.configuration import configuration
    credentials_path = get_credentials_path(configuration)
    google_sheets_client = configure_client(credentials_path)
    si_sheet = google_sheets_client.create(output_spreadsheet_name)
    # TODO: get collaborators from config
    si_sheet.share(configuration.admin.email, perm_type='user', role='writer')
    worksheet = si_sheet.sheet1
    worksheet.update_title(drive_config.statement_items_sheet_name)
    _format_worksheet(worksheet, ledger_config)
    return si_sheet, worksheet


def _format_worksheet(worksheet, ledger_config):
    worksheet.freeze(**ledger_config.freeze.toDict())
    for column_format in ledger_config.column_formats:
        worksheet.format(**column_format.toDict())


def _merge(statement_items, ledger_config, worksheet, account_collection):
    _, statement_items_for_gsheet = _statement_items_for_gsheet(statement_items)
    # list is processed multiple times so it is necessary to instantiate the generator here
    statement_items_for_gsheet = list(statement_items_for_gsheet)
    formula_templates = [template or "" for template in ledger_config.formula_templates]

    for account in account_collection:
        account_no = account._account_no
        rows_to_add = list(filter(lambda row: row[0] == account_no, statement_items_for_gsheet))
        if rows_to_add:
            first_account_cell = worksheet.find(account_no)
            assert first_account_cell.col == 1, "Did not expect to find account number except in column 1"
            insert_at = first_account_cell.row
            rows_with_formulae = [
                list(row_data) + [
                    formula_template.format(row_no=row_no, prev_row=row_no + 1)
                    for formula_template in formula_templates
                ]
                for row_no, row_data in enumerate(rows_to_add, insert_at)
            ]

            LOG.info(f"Inserting {len(rows_to_add)} rows for account {account_no} at row {insert_at}")

            insert_rows(worksheet, rows_with_formulae, insert_at, value_input_option="USER_ENTERED")
    _format_worksheet(worksheet, ledger_config)


def output_statement_items(
        module_name, configuration, drive_config, ledger_config, output_csv, output_spreadsheet, account_collection, statement_items
):
    if output_spreadsheet:
        gsheet = open_sheet(configuration, output_spreadsheet)
        if gsheet:
            import gspread
            worksheet_name = drive_config.statement_items_sheet_name
            try:
                worksheet = gsheet.worksheet(worksheet_name)
            except gspread.exceptions.WorksheetNotFound:
                worksheet = None
            if worksheet:
                LOG.info(f"Merging with existing worksheet, {worksheet_name}, on gsheet {output_spreadsheet}")
            else:
                worksheet = gsheet.add_worksheet(title=worksheet_name)
                LOG.info(f"Adding new sheet, {worksheet_name}, to existing gsheet {output_spreadsheet}")
            _merge(statement_items, ledger_config, worksheet, account_collection)
        else:
            _, worksheet = _new_sheet(module_name, drive_config, ledger_config, output_spreadsheet)
            LOG.info(f"Writing to new gsheet {output_spreadsheet}")
            _append(statement_items, worksheet)
    elif output_csv:
        with output_csv:
            statement_item_csv(statement_items, output_csv)
    else:
        with session_scope() as session:
            for statement_item in statement_items:
                session.add(statement_item)


def load_from_gsheet(configuration, export_folder, export_file, num_months):
    account_collection = get_accounts_from_sheet(configuration)

    loader = StatementLoader(StatementItem, account_collection)

    statement_item_exports = list(
        statement_item_export_files(__name__, configuration.gdrive, export_folder, export_file)
    )

    assert len(statement_item_exports) == 1, "Unexpected number of statement item export files"

    items = loader.load_from_statement(statement_item_exports[0])
    statement_items = StatementItemCollection(items) \
        .only_most_common_months(num_months) \
        .remove_net_zero_items()

    output_spreadsheet = configuration.gdrive.ledger_sheet_id
    output_statement_items(
        __name__,
        configuration,
        configuration.gdrive,
        configuration.ledger_sheet,
        None,
        output_spreadsheet,
        account_collection,
        statement_items
    )
