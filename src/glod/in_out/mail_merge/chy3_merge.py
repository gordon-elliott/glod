__copyright__ = "Copyright (c) Gordon Elliott 2020"

import logging
import os

from datetime import date
from decimal import Decimal
from tempfile import TemporaryDirectory

from a_tuin.db.session_scope import session_scope
from a_tuin.in_out.google_drive import (
    download_as_pdf,
    get_gdrive_service,
    get_gdocs_service,
    upload_to_gdrive,
    PDF_MIME_TYPE,
)
from a_tuin.in_out.google_docs import merge_letter, template_doc_properties
from a_tuin.in_out.pdf_merge import fill_form, concatenate

from glod.configuration import configuration
from glod.db.engine import engine  # required in order that db is bound
from glod.db import PPSQuery
from glod.in_out.mail_merge.letter_merge import _read_from_gsheet

LOG = logging.getLogger(__name__)

DONOR = "Name of Donor"
PPS = "PPSN"
POSTAL_ADDRESS = "Address incl. Eircode"
PHONE = "Phone No"
EMAIL = "Email Address"
CHARITY_NAME = "Name of eligible charity or other approved body"
VALID_FROM = "0"


def _merge_letters(
    gdrive,
    gdocs,
    temp_dir,
    template_file_id,
    template_filename,
    valid_from_tax_year,
    targets,
):
    for given_name, donor, pps, postal_address, phone, email, household_id in targets:
        LOG.info(f"Merging letter for {given_name}, household id: {household_id}")
        cover_letter_filename = f"cover.{household_id}.pdf"
        cover_letter_path = os.path.join(temp_dir, cover_letter_filename)
        replacements = dict(given_name=given_name)
        with merge_letter(
            gdrive, gdocs, template_file_id, replacements
        ) as merged_file_id:
            download_as_pdf(gdrive, merged_file_id, cover_letter_path)

        chy3_filename = f"chy3.{household_id}.pdf"
        chy3_file_path = os.path.join(temp_dir, chy3_filename)
        merge_data = {
            DONOR: donor,
            PPS: pps,
            POSTAL_ADDRESS: postal_address,
            PHONE: phone,
            EMAIL: email,
            CHARITY_NAME: configuration.charity.name,
            VALID_FROM: str(valid_from_tax_year),
        }
        fill_form(template_filename, chy3_file_path, merge_data)

        output_file = os.path.join(temp_dir, f"combined.{household_id}.pdf")
        concatenate([cover_letter_path, chy3_file_path], output_file)

        yield output_file


def merge_chy3_letters(
    template_filename, input_workbook_file_id, sheet_name, template_file_id
):
    current_year = date.today().year
    consider_last_n_years = int(configuration.tax.chy3.consider_last_n_years)
    last_n_years = tuple(
        range(current_year - consider_last_n_years + 1, current_year + 1)
    )
    valid_from_tax_year = current_year - 2001
    donation_threshold = Decimal(configuration.tax.chy3.minimum_donation)

    drive_config = configuration.gdrive
    gdrive = get_gdrive_service(configuration)
    gdocs = get_gdocs_service(configuration)
    template_file_id = drive_config.chy3_template_doc_id

    working_folder = "."
    # template_title, merge_fields = template_doc_properties(gdocs, template_file_id)
    template_title = "test"
    merge_fields = (
        "GIVEN_NAME",
        "DONOR",
        "PPS",
        "POSTAL_ADDRESS",
        "PHONE",
        "EMAIL",
        "HOUSEHOLD_ID",
    )
    LOG.info(f"Tags to merge from {template_title}: {', '.join(merge_fields)}")

    full_merge_pdf_filename = f"chy3_letters_from_{valid_from_tax_year}.pdf"

    targets = list(_read_from_gsheet(input_workbook_file_id, sheet_name, merge_fields))
    with TemporaryDirectory(
        dir=working_folder, prefix=f"{template_title}_merge_"
    ) as temp_dir:
        output_files = list(
            _merge_letters(
                gdrive,
                gdocs,
                temp_dir,
                template_file_id,
                template_filename,
                valid_from_tax_year,
                targets,
            )
        )

        full_merge_pdf_filepath = os.path.join(temp_dir, full_merge_pdf_filename)
        concatenate(output_files, full_merge_pdf_filepath)

        upload_to_gdrive(
            gdrive,
            full_merge_pdf_filepath,
            full_merge_pdf_filename,
            PDF_MIME_TYPE,
            configuration.charity.admin.email,
        )
