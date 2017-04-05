__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.io.gsheet_integration import get_gsheet_fields, load_class
from a_tuin.metadata import StringField, Mapping

from glod.db.subject import Subject
from glod.db.nominal_account import NominalAccountQuery


def subjects_from_gsheet(session, extract_from_detailed_ledger):
    nominal_account_collection = NominalAccountQuery(session).collection()

    class NominalAccountStringField(StringField):
        def conform_value(self, value):
            if not value:
                return None
            else:
                nominal_accounts = nominal_account_collection.lookup(value, '_code')
                return next(nominal_accounts)

    subject_gsheet = get_gsheet_fields(
        Subject,
        {
            'name': 'subject',
            'nominal account': 'rcb code',
        }
    )
    subject_gsheet['rcb code'] = NominalAccountStringField('rcb code')
    subject_mapping = Mapping(subject_gsheet, Subject.constructor_parameters)
    subjects = extract_from_detailed_ledger(
        'report lookups',
        'A3',
        ('subject', 'select vestry summary', 'easter vestry summary', 'rcb code')
    )
    load_class(session, subjects, subject_mapping, Subject)