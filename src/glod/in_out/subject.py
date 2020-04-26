__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.in_out.gsheet_integration import get_gsheet_fields, load_class
from a_tuin.metadata import Mapping

from glod.db.subject import Subject


def subjects_from_gsheet(session, extract_from_detailed_ledger):
    subject_gsheet = get_gsheet_fields(
        Subject,
        {
            'name': 'subject',
        }
    )
    subject_mapping = Mapping(subject_gsheet, Subject.constructor_parameters)
    subjects = extract_from_detailed_ledger(
        'report lookups',
        'A3',
        ('subject', 'select vestry summary', 'easter vestry summary')
    )
    load_class(session, subjects, subject_mapping, Subject)
