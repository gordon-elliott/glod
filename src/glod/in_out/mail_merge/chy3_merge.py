__copyright__ = "Copyright (c) Gordon Elliott 2020"

import logging
import os

from datetime import date
from tempfile import TemporaryDirectory

from a_tuin.in_out.google_drive import (
    download_as_pdf,
    get_gdrive_service,
    get_gdocs_service,
    upload_to_gdrive,
    PDF_MIME_TYPE,
)
from a_tuin.in_out.google_docs import merge_letter, template_doc_properties
from a_tuin.in_out.pdf_merge import fill_form, concatenate

from glod.in_out.mail_merge.letter_merge import read_from_gsheet

LOG = logging.getLogger(__name__)

REF = "ref"
DONOR = "Name of Donor"
PPS = "PPSN"
POSTAL_ADDRESS = "Address incl. Eircode"
PHONE = "Phone No"
EMAIL = "Email Address"
CHARITY_NAME = "Name of eligible charity or other approved body"
VALID_FROM = "0"

FORM_FIELDS = (DONOR, PPS, POSTAL_ADDRESS, PHONE, EMAIL)


def _merge_letters(
    configuration,
    gdrive,
    gdocs,
    temp_dir,
    template_file_id,
    template_filename,
    valid_from_tax_year,
    cover_merge_fields,
    targets,
):
    for target in targets:
        form_dict = dict(zip(FORM_FIELDS, target[:len(FORM_FIELDS)]))
        cover_dict = dict(zip(cover_merge_fields, target[-1 * len(cover_merge_fields):]))

        ref = cover_dict.get(REF)
        cover_letter_filename = f"cover.{ref}.pdf"
        cover_letter_path = os.path.join(temp_dir, cover_letter_filename)

        LOG.info(f"Merging letter for {cover_dict} to {cover_letter_path}.")

        with merge_letter(gdrive, gdocs, template_file_id, cover_dict) as merged_file_id:
            download_as_pdf(gdrive, merged_file_id, cover_letter_path)

        chy3_filename = f"chy3.{ref}.pdf"
        chy3_file_path = os.path.join(temp_dir, chy3_filename)
        merge_data = {
            CHARITY_NAME: configuration.charity.name,
            VALID_FROM: str(valid_from_tax_year),
        }
        merge_data.update(form_dict)
        fill_form(template_filename, chy3_file_path, merge_data)

        output_file = os.path.join(temp_dir, f"combined.{ref}.pdf")
        concatenate([cover_letter_path, chy3_file_path], output_file)

        yield output_file


def merge_chy3_letters(
    configuration, input_workbook_file_id, sheet_name, form_merge_fields, template_letter_file_id, empty_certificate_form
):
    if len(form_merge_fields) != len(FORM_FIELDS):
        raise ValueError(
            f"There are too many or too few form merge fields. {len(form_merge_fields)} found; {len(FORM_FIELDS)} expected."
        )

    current_year = date.today().year
    valid_from_tax_year = current_year - 2001

    gdrive = get_gdrive_service(configuration)
    gdocs = get_gdocs_service(configuration)

    working_folder = "."
    full_merge_pdf_filename = f"chy3_letters_from_{sheet_name}.pdf"
    _, cover_merge_fields = template_doc_properties(gdocs, template_letter_file_id)

    if REF not in cover_merge_fields:
        raise ValueError(f"Template cover letter must include a field titled '{REF}'.")

    merge_fields = form_merge_fields + cover_merge_fields

    targets = read_from_gsheet(configuration, input_workbook_file_id, sheet_name, merge_fields)
    with TemporaryDirectory(dir=working_folder, prefix=f"chy3_merge_") as temp_dir:
        output_files = list(
            _merge_letters(
                configuration,
                gdrive,
                gdocs,
                temp_dir,
                template_letter_file_id,
                empty_certificate_form,
                valid_from_tax_year,
                cover_merge_fields,
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
