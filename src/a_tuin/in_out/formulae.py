__copyright__ = 'Copyright(c) Gordon Elliott $today.year'
"""Common function for Google Sheets formulae"""


def _cell_dimension(index: str | int):
    return f'text({index}, "#")' if isinstance(index, str) else f'"{index}"'


def cell_reference(row: str | int, column: str | int):
    """Using a row and column, return a formula which references a cell. row and column may be 1-based indices
    or strings for dynamically calculating cell references (row() or column()) """
    row_str = _cell_dimension(row)
    column_str = _cell_dimension(column)
    return f'indirect(concatenate("R", {row_str}, "C", {column_str}), FALSE)'


def running_total(_, __=None):
    next_row = cell_reference("row()+1", "column()")
    previous_column = cell_reference("row()", "column()-1")
    return f'={next_row} + {previous_column}'
