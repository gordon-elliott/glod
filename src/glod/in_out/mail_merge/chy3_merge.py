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
    PDF_MIME_TYPE
)
from a_tuin.in_out.google_docs import merge_letter
from a_tuin.in_out.pdf_merge import fill_form, concatenate

from glod.configuration import configuration
from glod.db.engine import engine       # required in order that db is bound
from glod.db import PPSQuery

LOG = logging.getLogger(__name__)

DONOR = "Name of donor"
PPS = "PPS Number"
POSTAL_ADDRESS = "undefined"
PHONE = "Phone no"
EMAIL = "Email Address"
CHARITY_NAME = "Name of eligible charity or other approved body hereinafter referred to as an approved body"
VALID_FROM = "Text20"


def _merge_letters(gdrive, gdocs, temp_dir, template_file_id, template_filename, valid_from_tax_year, targets):
    for selected_member, person, household_org, address in targets:
        LOG.info(f"Merging letter for {person.name}, household id: {household_org.id}")
        cover_letter_filename = f"cover.{household_org.id}.pdf"
        cover_letter_path = os.path.join(temp_dir, cover_letter_filename)
        replacements = dict(given_name=person.given_name)
        with merge_letter(gdrive, gdocs, template_file_id, replacements) as merged_file_id:
            download_as_pdf(gdrive, merged_file_id, cover_letter_path)

        chy3_filename = f"chy3.{household_org.id}.pdf"
        chy3_file_path = os.path.join(temp_dir, chy3_filename)
        merge_data = {
            DONOR: selected_member.name_override if selected_member.name_override else person.name_without_title,
            PPS: selected_member.pps if selected_member.pps else '',
            POSTAL_ADDRESS: address.post_label(),
            PHONE: person.mobile if person.mobile else address.telephone,
            EMAIL: person.email,
            CHARITY_NAME: configuration.charity.name,
            VALID_FROM: str(valid_from_tax_year),
        }
        fill_form(template_filename, chy3_file_path, merge_data)

        output_file = os.path.join(temp_dir, f"combined.{household_org.id}.pdf")
        concatenate([cover_letter_path, chy3_file_path], output_file)

        yield output_file


def merge_chy3_letters(template_filename):
    current_year = date.today().year
    consider_last_n_years = int(configuration.tax.chy3.consider_last_n_years)
    last_n_years = tuple(range(current_year - consider_last_n_years + 1, current_year + 1))
    valid_from_tax_year = current_year - 1
    donation_threshold = Decimal(configuration.tax.chy3.minimum_donation)

    drive_config = configuration.gdrive
    gdrive = get_gdrive_service(configuration)
    gdocs = get_gdocs_service(configuration)
    template_file_id = drive_config.chy3_template_doc_id

    working_folder = '.'
    full_merge_pdf_filename = f"chy3_letters_from_{valid_from_tax_year}.pdf"
    with session_scope() as session:
        targets = PPSQuery(session).chy3_completion_targets(last_n_years, donation_threshold)
        with TemporaryDirectory(dir=working_folder, prefix='chy3_merge_') as temp_dir:
            output_files = list(
                _merge_letters(
                    gdrive, gdocs, temp_dir, template_file_id,
                    template_filename, valid_from_tax_year, targets
                )
            )

            full_merge_pdf_filepath = os.path.join(temp_dir, full_merge_pdf_filename)
            concatenate(output_files, full_merge_pdf_filepath)

            upload_to_gdrive(
                gdrive, full_merge_pdf_filepath, full_merge_pdf_filename,
                PDF_MIME_TYPE, configuration.charity.admin.email
            )
