__copyright__ = 'Copyright(c) Gordon Elliott 2022'
""" Utilities to manipulate Google Docs
"""

import re
from typing import List, Tuple

from contextlib import contextmanager


TAG_OPENING = '<<'
TAG_CLOSING = '>>'


def _read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')


def _read_structural_elements(elements):
    """Recurses through a list of Structural Elements to read a document's text where text may be
        in nested elements.

        Args:
            elements: a list of Structural Elements.
    """
    text = ''
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += _read_paragraph_element(elem)
        elif 'table' in value:
            # The text in table cells are in nested Structural Elements and tables may be
            # nested.
            table = value.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += _read_structural_elements(cell.get('content'))
        elif 'tableOfContents' in value:
            # The text in the TOC is also in a Structural Element.
            toc = value.get('tableOfContents')
            text += _read_structural_elements(toc.get('content'))
    return text


def template_doc_properties(gdocs, template_file_id) -> Tuple[str, List[str]]:
    """Find the merge tags in a template Google Doc."""

    doc = gdocs.documents().get(documentId=template_file_id).execute()
    doc_content = doc.get('body').get('content')
    title = doc.get('title')
    text = _read_structural_elements(doc_content)

    for section_name in ['headers', 'footers']:
        doc_section = doc.get(section_name, {})
        for section in doc_section.values():
            doc_content = section.get('content')
            if doc_content:
                text += _read_structural_elements(doc_content)

    return title, re.findall(r"<<([^<]*)>>", text)


@contextmanager
def merge_letter(gdrive, gdocs, template_file_id, replacements):
    body = {'name': 'Merged form letter'}
    merged_file_id = gdrive.files().copy(
        body=body, fileId=template_file_id, fields='id', supportsAllDrives=True
    ).execute().get('id')
    try:
        replacement_command = [{'replaceAllText': {
            'containsText': {
                'text': ''.join((TAG_OPENING, key, TAG_CLOSING)),
                'matchCase': True,
            },
            'replaceText': value,
        }} for key, value in replacements.items()]

        gdocs.documents().batchUpdate(body={'requests': replacement_command}, documentId=merged_file_id, fields='').execute()

        yield merged_file_id
    finally:
        gdrive.files().delete(fileId=merged_file_id)
