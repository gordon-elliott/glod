__copyright__ = 'Copyright(c) Gordon Elliott 2022'
""" Mail merge for CHY3 forms and cover letters
"""

import argparse
import logging
import sys

from glod.in_out.mail_merge.letter_merge import merge_letters
from glod.configuration import configuration

LOG = logging.getLogger(__file__)
logging.basicConfig(level=logging.DEBUG)


def do_merge(input_workbook_file_id, sheet_name, template_file_id):
    try:
        merge_letters(configuration, input_workbook_file_id, sheet_name, template_file_id)
    except Exception as ex:
        LOG.exception(ex)
        return 1

    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Mail merge for letters'
    )
    parser.add_argument('input_workbook_file_id', type=str)
    parser.add_argument('sheet_name', type=str)
    parser.add_argument('template_file_id', type=str)
    args = parser.parse_args()

    sys.exit(do_merge(
        args.input_workbook_file_id, args.sheet_name, args.template_file_id
    ))
