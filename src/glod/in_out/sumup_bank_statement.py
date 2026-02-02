__copyright__ = 'Copyright(c) Gordon Elliott $today.year'
"""Extract Sumup transactions, fees and payouts into spreadsheet"""

from collections import defaultdict
from datetime import datetime, date, timezone
from typing import Any

from sumup import APIError
from sumup import Sumup
from sumup.payouts import ListPayoutsV1Params
from sumup.transactions import ListTransactionsV21Params

from a_tuin.in_out.formulae import cell_reference, running_total
from a_tuin.in_out.google_sheets import insert_rows, open_spreadsheet, open_worksheet

TRANSACTION_LIMIT = 1000
SUCCESSFUL_STATUS = "SUCCESSFUL"
FEE_TRANSACTION_TYPE = "FEE"
SUMUP_REGIME_START = datetime(2025, 1, 1, tzinfo=timezone.utc)
BASE_ORDINAL_DAY = datetime(1899, 12, 30).toordinal()


def _created_day(key: str, value_dict: dict):
    timestamp: datetime = value_dict.get("timestamp")
    return date(timestamp.year, timestamp.month, timestamp.day).isoformat()


def _year(key: str, value_dict: dict):
    timestamp: datetime = value_dict.get("timestamp")
    return timestamp.year


def _month(key: str, value_dict: dict):
    timestamp: datetime = value_dict.get("timestamp")
    return timestamp.month


def _day(key: str, value_dict: dict):
    timestamp: datetime = value_dict.get("timestamp")
    return timestamp.day


def _day_of_week(key: str, value_dict: dict):
    timestamp: datetime = value_dict.get("timestamp")
    return f'=vlookup({timestamp.weekday()}, python_days_of_the_week, 2, TRUE)'


def _time_of_day(key: str, value_dict: dict):
    timestamp: datetime = value_dict.get("timestamp")
    return f'=vlookup({timestamp.hour}, times_of_day, 2, TRUE)'


def _subject(key: str, value_dict: dict):
    timestamp: datetime = value_dict.get("timestamp")
    gsheet_day_ordinal = timestamp.toordinal() - BASE_ORDINAL_DAY
    amount = value_dict.get("amount")
    day_of_week_cell = cell_reference("row()", _transaction_column_sheet_index("_f_day_of_week"))
    time_of_day_cell = cell_reference("row()", _transaction_column_sheet_index("_f_time_of_day"))
    if amount < 0:
        return '=negative_amount'
    else:
        return f'=iferror(vlookup(concatenate({day_of_week_cell}, "|", {time_of_day_cell}), regular_subject_table, 2, FALSE), iferror(vlookup(concatenate({gsheet_day_ordinal}, "|", {time_of_day_cell}), subject_table, 2, FALSE), default_subject))'


def _signed_amount(key: str, value_dict: dict):
    amount_cell = cell_reference("row()", _transaction_column_sheet_index("amount"))
    type_cell = cell_reference("row()", _transaction_column_sheet_index("type"))
    return f'=if({type_cell}="PAYMENT", 1, -1)*{amount_cell}'


transaction_formulae = {
    "_f_created_day": _created_day,
    "_f_year": _year,
    "_f_month": _month,
    "_f_day": _day,
    "_f_day_of_week": _day_of_week,
    "_f_time_of_day": _time_of_day,
    "_f_subject": _subject,
    "_f_signed_amount": _signed_amount,
    "_f_balance": running_total,
}


def _empty(key: str, value_dict: dict):
    return ""


def _date_obj_to_iso(key: str, value_dict: dict):
    timestamp: datetime = value_dict.get(key)
    return timestamp.isoformat()


def _get(key: str, value_dict: dict):
    return value_dict.get(key)


transaction_dotted_paths = {
                               "id": _get,
                               "currency": _get,
                               "amount": _get,
                               "product_summary": _get,
                               "status": _get,
                               "type": _get,
                               "user": _get,
                               "timestamp": _date_obj_to_iso,
                               "client_transaction_id": _get,
                               "transaction_code": _get,
                               "transaction_id": _get,
                           } | transaction_formulae

transaction_column_indices = {c: i for i, c in enumerate(transaction_dotted_paths.keys())}
amount_column_index = transaction_column_indices["amount"]
type_column_index = transaction_column_indices["type"]


def _transaction_column_sheet_index(column_name: str) -> int:
    return transaction_column_indices[column_name] + 1


def _payouts_created_day(key: str, value_dict: dict):
    return value_dict.get("date").isoformat()


def _payouts_year(key: str, value_dict: dict):
    date_ = value_dict.get("date")
    return date_.year


def _payouts_month(key: str, value_dict: dict):
    date_ = value_dict.get("date")
    return date_.month


def _payouts_day(key: str, value_dict: dict):
    date_ = value_dict.get("date")
    return date_.day


def _payouts_day_of_week(key: str, value_dict: dict):
    date_ = value_dict.get("date")
    return f'=vlookup({date_.weekday()}, python_days_of_the_week, 2, TRUE)'


def _payouts_subject(key: str, value_dict: dict):
    return '=negative_amount'


payouts_dotted_paths = {
    "reference": _get,
    "currency": _get,
    "amount": _empty,
    "product_summary": _empty,
    "status": _get,
    "type": _get,
    "user": _empty,
    "date": _date_obj_to_iso,
    "client_transaction_id": _empty,
    "transaction_code": _empty,
    "transaction_id": _empty,
    "_f_created_day": _payouts_created_day,
    "_f_year": _payouts_year,
    "_f_month": _payouts_month,
    "_f_day": _payouts_day,
    "_f_day_of_week": _payouts_day_of_week,
    "_f_time_of_day": _empty,
    "_f_subject": _payouts_subject,
    "_f_signed_amount": _signed_amount,
    "_f_balance": running_total,
}


def _transform(entity, dotted_paths: dict) -> list:
    value_dict = entity.model_dump(include=dotted_paths.keys())
    transformed = [
        transform(k, value_dict)
        for k, transform in dotted_paths.items()
    ]
    return transformed


def _payouts(
    merchant_code: str, sumup: Sumup, start_timestamp: datetime, end_timestamp: datetime, stop_on_id: str
) -> tuple[dict[Any, Any], list[Any]]:
    payout_amounts = defaultdict(int)
    payout_fees = {}
    try:
        payouts = sumup.payouts.list(
            merchant_code,
            params=ListPayoutsV1Params(
                start_date=start_timestamp.date(),
                end_date=end_timestamp.date(),
                limit=TRANSACTION_LIMIT,
                order="desc"
            )
        )  # , oldest_time="2025-12-02T00:00:00.000Z"))

    except APIError as e:
        print(f"{e}, {e.status} {e.body}")
        raise

    for payout in payouts:
        if payout.reference == stop_on_id:
            # stop processing when we reach the last line that was previously in the sheet
            break
        payout_fees[payout.transaction_code] = payout.fee
        if payout.status == SUCCESSFUL_STATUS:
            payout_values = _transform(payout, payouts_dotted_paths)
            payout_tuple = tuple(payout_values)
            payout_amounts[payout_tuple] += payout.amount

    successful_payouts = []
    for payout_tuple, amount in payout_amounts.items():
        payout_values = list(payout_tuple)
        payout_values[amount_column_index] = amount
        successful_payouts.append(payout_values)
    return payout_fees, successful_payouts


def _filter_sumup_transaction(transaction, start_timestamp: datetime, end_timestamp: datetime) -> bool:
    return transaction.status == SUCCESSFUL_STATUS and start_timestamp < transaction.timestamp < end_timestamp


def _transactions(
    merchant_code: str, sumup: Sumup, payout_fees: dict[Any, Any], start_timestamp: datetime, end_timestamp: datetime,
    stop_on_id: str
) -> list[Any]:
    try:
        result = sumup.transactions.list(
            merchant_code, params=ListTransactionsV21Params(
                limit=TRANSACTION_LIMIT,
                order="descending"
            )
        )  # , oldest_ref=last_transaction_code))
    except APIError as e:
        print(f"{e}, {e.status} {e.body}")
        raise

    transactions = []
    for transaction in result.items:
        if transaction.id == stop_on_id:
            # stop processing when we reach the last line that was previously in the sheet
            break
        if _filter_sumup_transaction(transaction, start_timestamp, end_timestamp):
            transaction_values = _transform(transaction, transaction_dotted_paths)
            if transaction.transaction_code in payout_fees:
                transactions.append(transaction_values)  # only output transactions for which there has been a payout
                fee_transaction = list(transaction_values)
                fee_transaction[type_column_index] = FEE_TRANSACTION_TYPE
                fee_transaction[amount_column_index] = payout_fees[transaction.transaction_code]
                transactions.append(fee_transaction)
    return transactions


def load_from_sumup_api(
    configuration, merchant_code: str, api_key: str, output_spreadsheet: str, worksheet_name: str, end_timestamp: datetime
):
    sumup_gsheet = open_spreadsheet(configuration, output_spreadsheet)
    sumup_worksheet = open_worksheet(sumup_gsheet, worksheet_name)

    timestamp_column_index = _transaction_column_sheet_index("timestamp")
    last_created_str = max(sumup_worksheet.col_values(timestamp_column_index)[1:])
    last_created = datetime.fromisoformat(last_created_str).replace(
        tzinfo=timezone.utc
    ) if last_created_str else SUMUP_REGIME_START

    id_column_index = _transaction_column_sheet_index("id")
    id_values = sumup_worksheet.col_values(id_column_index)
    last_id = id_values[1] if len(id_values) > 1 else None

    print(f"Loading statement items between {last_created} and {end_timestamp} as far as {last_id}.")

    sumup = Sumup(api_key)

    payout_fees, successful_payouts = _payouts(merchant_code, sumup, last_created, end_timestamp, last_id)

    if not payout_fees:
        print("No payouts found. Workbook not updated.")
        return

    transactions = _transactions(merchant_code, sumup, payout_fees, last_created, end_timestamp, last_id)

    if not transactions:
        print("No transactions found. Workbook not updated.")
        return

    timestamp_tuple_index = transaction_column_indices["timestamp"]
    by_date = sorted(transactions + successful_payouts, key=lambda txn: txn[timestamp_tuple_index], reverse=True)

    insert_rows(sumup_worksheet, by_date, 2, value_input_option="USER_ENTERED")
