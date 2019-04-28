__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""
import logging

from gspread import authorize
from gspread.utils import a1_to_rowcol
from oauth2client.service_account import ServiceAccountCredentials


LOG = logging.getLogger(__name__)
ROWS_PER_FETCH = 500


def configure_client(credentials_path):
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    return authorize(credentials)


def is_formula(cell):
    input_value = cell.input_value
    return input_value and input_value[0] == '='


def _sheet_rows(worksheet, num_columns, first_row, first_column):
    for first_row_in_range in range(first_row, worksheet.row_count, ROWS_PER_FETCH):
        previous_column = 0
        last_row_in_range = min(first_row_in_range + ROWS_PER_FETCH - 1, worksheet.row_count)
        last_column_in_range = first_column + num_columns - 1
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

    header = []
    header_row, first_column = a1_to_rowcol(starting_cell)
    for column in range(first_column, worksheet.col_count + first_column):
        contents = worksheet.cell(header_row, column).value
        if contents:
            header.append(contents)
        else:
            break

    assert tuple(header[:len(column_names)]) == column_names, 'Header does not match desired columns'

    LOG.info('Reading %r from %s' % (column_names, worksheet_title))

    first_row = header_row + 1
    for row_cells in _sheet_rows(worksheet, len(column_names), first_row, first_column):
        values = tuple(cell.value for cell in row_cells)
        if any(values):
            yield values
        else:
            # stop when we reach a blank line
            break
