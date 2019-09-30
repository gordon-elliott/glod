__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""
import logging

from gspread import Client
from gspread.utils import a1_to_rowcol
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

LOG = logging.getLogger(__name__)
ROWS_PER_FETCH = 1000
SCOPES = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]


def configure_client(credentials_path):
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    scoped_credentials = credentials.with_scopes(SCOPES)
    session = AuthorizedSession(scoped_credentials)
    gsheet_client = Client(scoped_credentials, session)
    return gsheet_client


def is_formula(cell):
    input_value = cell.input_value
    return input_value and input_value[0] == '='


def _sheet_rows(worksheet, first_row, first_column, last_column_in_range):
    for first_row_in_range in range(first_row, worksheet.row_count, ROWS_PER_FETCH):
        previous_column = 0
        last_row_in_range = min(first_row_in_range + ROWS_PER_FETCH - 1, worksheet.row_count)
        LOG.info('Fetching worksheet columns %d to %d, rows %d to %d' % (
            first_column, last_column_in_range, first_row_in_range, last_row_in_range
        ))
        row = []
        for cell in worksheet.range(first_row_in_range, first_column, last_row_in_range, last_column_in_range):
            if cell.col < previous_column:
                yield row
                row = []
            row.append(cell)
            previous_column = cell.col

        if row:
            yield row


def extract_table(spreadsheet, worksheet_title, starting_cell, column_names):

    worksheet = spreadsheet.worksheet(worksheet_title)

    header_row, first_column = a1_to_rowcol(starting_cell)
    num_columns = len(column_names)
    last_column = first_column + num_columns - 1
    header = tuple(
        cell.value
        for cell in worksheet.range(header_row, first_column, header_row, last_column)
    )
    assert header == column_names, 'Header does not match desired columns. %r != %r' % (header, column_names)

    LOG.info(f'Reading {column_names} from {worksheet_title}')

    first_row = header_row + 1
    for row_cells in _sheet_rows(worksheet, first_row, first_column, last_column):
        values = tuple(cell.value for cell in row_cells)
        if any(values):
            yield values
        else:
            # stop when we reach a blank line
            break
