__copyright__ = 'Copyright(c) Gordon Elliott 2020'

""" Mail merge for CHY3 forms and cover letters
"""


import argparse
import logging
import sys

from datetime import date
from decimal import Decimal

from a_tuin.db.session_scope import session_scope
from glod.db.engine import engine       # required in order to connect db

from glod.in_out.pdf_merge import fill_form
from glod.db.pps import PPSQuery

LOG = logging.getLogger(__file__)
logging.basicConfig(level=logging.DEBUG)


DONOR = "Name of donor"
PPS = "PPS Number"
POSTAL_ADDRESS = "undefined"
PHONE = "Phone no"
EMAIL = "Email Address"
CHARITY_NAME = "Name of eligible charity or other approved body hereinafter referred to as an approved body"
VALID_FROM = "Text20"

FIELDS = (
    DONOR,
    PPS,
    POSTAL_ADDRESS,
    PHONE,
    EMAIL,
    CHARITY_NAME,
    VALID_FROM,
)


def do_merge(template_filename):
    try:
        current_year = date.today().year
        last_3_years = tuple(range(current_year - 2, current_year + 1))
        donation_threshold = Decimal(250.0)
        with session_scope() as session:
            targets = PPSQuery(session).chy3_completion_targets(last_3_years, donation_threshold)
            for selected_member, person, household_org, address in targets:
                merge_data = {
                    DONOR: selected_member.name_override if selected_member.name_override else person.name_without_title,
                    PPS: selected_member.pps if selected_member.pps else '',
                    POSTAL_ADDRESS: address.post_label(),
                    PHONE: person.mobile if person.mobile else address.telephone,
                    EMAIL: person.email,
                    CHARITY_NAME: "Christ Church Delgany",
                    VALID_FROM: str(current_year),
                }
                # TODO use a temporary folder
                # TODO merge with cover letters
                # TODO merge into single PDF - pdftk *.pdf cat output combined.pdf
                file_name = f"./merge0/merged.{household_org.id}.pdf"
                fill_form(template_filename, file_name, merge_data)
    except Exception as ex:
        LOG.exception(ex)
        return 1

    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Mail merge for CHY3 forms and cover letters'
    )
    parser.add_argument('template_filename', type=str)
    # parser.add_argument('export_folder', type=str)
    # parser.add_argument('export_file', type=str)
    # parser.add_argument('out_spreadsheet', type=str)
    # parser.add_argument('--account_file', type=str, required=False)
    # parser.add_argument('--num_months', type=int, required=False, default=1)
    args = parser.parse_args()

    sys.exit(do_merge(
        args.template_filename
    ))
