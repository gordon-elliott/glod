__copyright__ = "Copyright (c) Gordon Elliott 2020"

import logging
import os
from datetime import date
from tempfile import TemporaryDirectory
from uuid import uuid4

from a_tuin.in_out.google_drive import (
    download_as_pdf,
    get_gdrive_service,
    get_gdocs_service,
    upload_to_gdrive,
    PDF_MIME_TYPE
)
from a_tuin.in_out.google_docs import merge_letter, template_doc_properties
from a_tuin.in_out.google_sheets import extract_from_sheet
from a_tuin.in_out.pdf_merge import concatenate
from glod.configuration import configuration

LOG = logging.getLogger(__name__)


def _merge_letters(gdrive, gdocs, temp_dir, template_file_id, targets, column_names):
    for row_data in targets:
        uuid = uuid4()
        letter_filename = f"merge.{uuid}.pdf"
        letter_path = os.path.join(temp_dir, letter_filename)
        replacements = dict(zip(column_names, row_data))

        LOG.info(f"Merging letter with {replacements} -> {letter_path}")
        with merge_letter(gdrive, gdocs, template_file_id, replacements) as merged_file_id:
            download_as_pdf(gdrive, merged_file_id, letter_path)

        yield letter_path


def _read_from_gsheet(input_workbook_file_id, sheet_name, merge_fields):
    extract_from_workbook = extract_from_sheet(configuration, input_workbook_file_id)
    parishioners = extract_from_workbook(sheet_name, 'A1', merge_fields)
    return parishioners


def merge_letters(input_workbook_file_id, sheet_name, template_file_id):
    current_year = date.today().year

    gdrive = get_gdrive_service(configuration)
    gdocs = get_gdocs_service(configuration)

    working_folder = '.'
    template_title, merge_fields = template_doc_properties(gdocs, template_file_id)
    LOG.info(f"Tags to merge from {template_title}: {', '.join(merge_fields)}")

    full_merge_pdf_filename = f"{template_title}_{sheet_name}_{current_year}.pdf"
    targets = _read_from_gsheet(input_workbook_file_id, sheet_name, merge_fields)
    with TemporaryDirectory(dir=working_folder, prefix=f'{template_title}_merge_') as temp_dir:
        output_files = list(
            _merge_letters(
                gdrive, gdocs, temp_dir, template_file_id,
                targets, merge_fields
            )
        )

        full_merge_pdf_filepath = os.path.join(temp_dir, full_merge_pdf_filename)
        concatenate(output_files, full_merge_pdf_filepath)

        upload_to_gdrive(
            gdrive, full_merge_pdf_filepath, full_merge_pdf_filename,
            PDF_MIME_TYPE, configuration.charity.admin.email
        )
