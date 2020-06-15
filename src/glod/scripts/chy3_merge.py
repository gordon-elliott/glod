__copyright__ = 'Copyright(c) Gordon Elliott 2020'

""" Mail merge for CHY3 forms and cover letters
"""

import argparse
import logging
import sys

from glod.in_out.mail_merge.chy3_merge import merge_chy3_letters

LOG = logging.getLogger(__file__)
logging.basicConfig(level=logging.DEBUG)


def do_merge(template_filename):
    try:
        merge_chy3_letters(template_filename)
    except Exception as ex:
        LOG.exception(ex)
        return 1

    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Mail merge for CHY3 forms and cover letters'
    )
    parser.add_argument('template_filename', type=str)
    args = parser.parse_args()

    sys.exit(do_merge(
        args.template_filename
    ))
