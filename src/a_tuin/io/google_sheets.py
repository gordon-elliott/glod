__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from gspread import authorize
from gspread.utils import a1_to_rowcol
from oauth2client.service_account import ServiceAccountCredentials


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


def extract_table(spreadsheet, worksheet_title, starting_cell, column_names):

    worksheet = spreadsheet.worksheet(worksheet_title)

    header = []
    header_row, first_column = a1_to_rowcol(starting_cell)
    for column in range(first_column, worksheet.col_count):
        contents = worksheet.cell(header_row, column).value
        if contents:
            header.append(contents)
        else:
            break

    assert tuple(header[:len(column_names)]) == column_names, 'Header does not match desired columns'

    for row in range(header_row + 1, worksheet.row_count):
        row_cells = worksheet.range(row, first_column, row, first_column + len(column_names))
        values = tuple(cell.input_value for cell in row_cells if not is_formula(cell))
        if any(values):
            yield values
        else:
            # stop when we reach a blank line
            break


