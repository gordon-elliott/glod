__copyright__ = 'Copyright(c) Gordon Elliott 2026'
"""Load bank statement from Stripe API into a spreadsheet"""

from datetime import datetime
from typing import Any, Callable

import stripe

from a_tuin.in_out.formulae import cell_reference, running_total
from a_tuin.in_out.google_sheets import insert_rows, open_spreadsheet, open_worksheet
from glod.configuration import configuration


def de_nest(dotted_path: str, nested_dict: dict, convert: Callable):
    if dotted_path.startswith("_f"):
        return convert(nested_dict)
    if "." not in dotted_path:
        return convert(nested_dict.get(dotted_path))
    head, tail = dotted_path.split(".", 1)
    if head in nested_dict:
        return de_nest(tail, nested_dict[head], convert)
    else:
        return None


def flatten_nested_dict(nested_dict: dict, dotted_paths: dict) -> list[Any]:
    return [
        de_nest(dotted_path, nested_dict, convert)
        for dotted_path, convert in dotted_paths.items()
    ]


def _date(epoch_seconds):
    return datetime.fromtimestamp(epoch_seconds).isoformat()


def _date_with_dls(epoch_seconds):
    return datetime.fromtimestamp(epoch_seconds).astimezone(GMT).replace(tzinfo=None).isoformat()


def _currency(amount):
    return amount / 100


def _no_op(x):
    return x


def _date_cell():
    return cell_reference("row()", _column_sheet_index("created"))


def _created_day(_):
    return f'=datevalue(left({_date_cell()}, 10))'


def _year(_):
    return f'=year({_date_cell()})'


def _month(_):
    return f'=month({_date_cell()})'


def _day(_):
    return f'=day({_date_cell()})'


def _day_of_week(_):
    return f'=vlookup(weekday({_date_cell()}), sheets_days_of_the_week, 3, TRUE)'


def _time_of_day(_):
    return f'=vlookup(hour({_date_cell()}), times_of_day, 2, TRUE)'


def _signed_fee(_):
    fee_cell = cell_reference("row()", _column_sheet_index("fee"))
    return f'=-1*{fee_cell}'


def _subject(_):
    amount_cell = cell_reference("row()", _column_sheet_index("amount"))
    date_only_cell = cell_reference("row()", _column_sheet_index("_f_created_day"))
    time_of_day_cell = cell_reference("row()", _column_sheet_index("_f_time_of_day"))
    return f'=if({amount_cell}<0, negative_amount, iferror(vlookup(concatenate({date_only_cell}, "|", {time_of_day_cell}), subject_table, 2, FALSE), default_subject))'


stripe_dotted_paths = {
    "id": _no_op,
    "created": _date,
    "available_on": _date,
    "currency": _no_op,
    "amount": _currency,
    "fee": _currency,
    "net": _currency,
    "_f_balance": running_total,
    "balance_type": _no_op,
    "reporting_category": _no_op,
    "status": _no_op,
    "type": _no_op,
    "description": _no_op,
    "source.customer.object": _no_op,
    "source.customer.id": _no_op,
    "source.customer.email": _no_op,
    "source.customer.name": _no_op,
    "_f_created_day": _created_day,
    "_f_year": _year,
    "_f_month": _month,
    "_f_day": _day,
    "_f_day_of_week": _day_of_week,
    "_f_time_of_day": _time_of_day,
    "_f_signed_fee": _signed_fee,
    "_f_subject": _subject,
}

column_indices = {c: i for i, c in enumerate(stripe_dotted_paths.keys())}
status_column_index = column_indices["status"]


def _column_sheet_index(column_name: str) -> int:
    return column_indices[column_name] + 1


def is_available(balance_transaction: dict) -> bool:
    status = balance_transaction[status_column_index]
    return status == "available"


def load_from_stripe_api(api_key: str, output_spreadsheet: str, worksheet_name: str):
    gsheet = open_spreadsheet(configuration, output_spreadsheet)
    worksheet = open_worksheet(gsheet, worksheet_name)

    created_column_index = _column_sheet_index("created")
    last_created_str = max(worksheet.col_values(created_column_index)[1:])
    last_created = datetime.fromisoformat(last_created_str)

    stripe.api_key = api_key
    balance_transactions = stripe.BalanceTransaction.list(
        created={"gt": int(last_created.timestamp())},
        expand=["data.source", "data.source.customer"]
    )
    gathered_transactions = list(balance_transactions.auto_paging_iter())

    all_statuses = [
        flatten_nested_dict(balance_transaction, stripe_dotted_paths)
        for balance_transaction in gathered_transactions
    ]
    # use any transactions after the first pending one
    rows_to_add = []
    for row in reversed(all_statuses):
        if is_available(row):
            rows_to_add.insert(0, row)
        else:
            break

    insert_rows(worksheet, rows_to_add, 2, value_input_option="USER_ENTERED")
