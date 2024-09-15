__copyright__ = 'Copyright(c) Gordon Elliott 2020'

""" Mail merge for CHY3 forms and cover letters
"""

import argparse
import logging
import sys

from glod.configuration import configuration
from glod.in_out.mail_merge.chy3_merge import merge_chy3_letters

LOG = logging.getLogger(__file__)
logging.basicConfig(level=logging.DEBUG)

MERGE_FIELDS = (
    "GIVEN_NAME",
    "DONOR",
    "PPS",
    "POSTAL_ADDRESS",
    "PHONE",
    "EMAIL",
    "HOUSEHOLD_ID",
    "REF",
)


def do_merge(empty_certificate_form, input_workbook_file_id, sheet_name, template_letter_file_id):
    try:
        merge_chy3_letters(
            configuration, input_workbook_file_id, sheet_name, MERGE_FIELDS, template_letter_file_id, empty_certificate_form
        )
    except Exception as ex:
        LOG.exception(ex)
        return 1

    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Mail merge for CHY3 forms and cover letters'
    )
    parser.add_argument('empty_certificate_form', type=str)
    parser.add_argument('input_workbook_file_id', type=str)
    parser.add_argument('sheet_name', type=str)
    parser.add_argument('template_letter_file_id', type=str)
    args = parser.parse_args()

    sys.exit(do_merge(
        args.empty_certificate_form, args.input_workbook_file_id, args.sheet_name, args.template_letter_file_id
    ))
