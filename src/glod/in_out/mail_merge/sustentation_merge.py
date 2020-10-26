__copyright__ = "Copyright (c) Gordon Elliott 2020"

import logging
import os
from datetime import date
from tempfile import TemporaryDirectory

from a_tuin.in_out.google_drive import (
    merge_cover_letter,
    download_as_pdf,
    get_gdrive_service,
    get_gdocs_service,
    upload_to_gdrive,
    PDF_MIME_TYPE
)
from a_tuin.in_out.google_sheets import extract_from_sheet
from a_tuin.in_out.pdf_merge import concatenate
from glod.configuration import configuration

LOG = logging.getLogger(__name__)


def _merge_letters(gdrive, gdocs, temp_dir, template_file_id, targets):
    for household_id, ref, titles in targets:
        letter_filename = f"sustentation.{household_id}.pdf"
        letter_path = os.path.join(temp_dir, letter_filename)
        replacements = dict(ref=ref, titles=titles)

        LOG.info(f"Merging letter for household id {household_id}, {titles} -> {letter_path}")
        with merge_cover_letter(gdrive, gdocs, template_file_id, replacements) as merged_file_id:
            download_as_pdf(gdrive, merged_file_id, letter_path)

        yield letter_path


def _read_from_gsheet(input_workbook_file_id, sheet_name):
    extract_from_workbook = extract_from_sheet(configuration, input_workbook_file_id)
    parishioners = extract_from_workbook(sheet_name, 'A1', ('household_id', 'ref', 'titles'))
    return parishioners


def merge_sustentation_letters(input_workbook_file_id, sheet_name, template_file_id):
    current_year = date.today().year

    gdrive = get_gdrive_service(configuration)
    gdocs = get_gdocs_service(configuration)

    working_folder = '.'
    full_merge_pdf_filename = f"sustentation_letters_{sheet_name}_{current_year}.pdf"

    targets = _read_from_gsheet(input_workbook_file_id, sheet_name)
    with TemporaryDirectory(dir=working_folder, prefix='sustentation_merge_') as temp_dir:
        output_files = list(
            _merge_letters(gdrive, gdocs, temp_dir, template_file_id, targets)
        )

        full_merge_pdf_filepath = os.path.join(temp_dir, full_merge_pdf_filename)
        concatenate(output_files, full_merge_pdf_filepath)

        upload_to_gdrive(
            gdrive, full_merge_pdf_filepath, full_merge_pdf_filename,
            PDF_MIME_TYPE, configuration.charity.admin.email
        )
