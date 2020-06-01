__copyright__ = 'Copyright(c) Gordon Elliott 2020'

from subprocess import run

""" Mail merge for CHY3 forms and cover letters
"""


import argparse
import logging
import sys

from glod.configuration import configuration

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

SAMPLE = {
    DONOR: "Joe Bloggs",
    PPS: "998989C",
    POSTAL_ADDRESS: "TeeMoKree,\n4 Main St,\nTownland,\nNewtown,\nCo Wicklow",
    PHONE: "9380830",
    EMAIL: "joseph.mary.bloggs@example.com",
    CHARITY_NAME: "Christ Church Delgany",
    VALID_FROM: "2020",
}

FDF_HEADER = """%FDF-1.2
%âãÏÓ
1 0 obj 
<< /FDF 
<< /Fields [
"""

FDF_FOOTER = """
] >> >>
endobj 
trailer
<< /Root 1 0 R >>
%%EOF
"""


def fill_forms(template_filename, output_path):
    fdf_str = generate_fdf(SAMPLE)
    fill_form(template_filename, fdf_str, output_path)


def generate_fdf(data):
    fields = "\n".join(fdf_fields(data))
    return f"{FDF_HEADER}{fields}{FDF_FOOTER}"


def fdf_fields(data):
    for field_name, value in data.items():
        yield f"<< /T ({field_name}) /V ({value}) >>"


def fill_form(input_path, fdf, output_path):
    cmd = ["pdftk", input_path, "fill_form", "-", "output", output_path, "flatten"]
    run(cmd, input=fdf.encode("utf-8"), check=True)


def do_merge(template_filename):
    try:
        fill_forms(template_filename, "merged.0.pdf")
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
