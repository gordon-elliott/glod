__copyright__ = 'Copyright(c) Gordon Elliott 2017'

from datetime import date, datetime
from decimal import Decimal


def strip_commas(value, _):
    return value.replace(',', '') if value else None


def strip_commas_and_spaces(value, _):
    return value.replace(',', '').strip() if value else None


def cast_dmy_date_from_string(value, _):
    return date.fromtimestamp(datetime.strptime(value, '%d/%m/%Y').timestamp())


def cast_ymd_date_from_string(value, _):
    return date.fromtimestamp(datetime.strptime(value, '%Y-%m-%d').timestamp())


def negate(value, _):
    if value:
        return Decimal(value) * -1
    return None
