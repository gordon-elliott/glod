__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.io.gsheet_integration import get_gsheet_fields, load_class
from a_tuin.metadata import (
    Mapping,
)

from glod.db.parishioner import Parishioner, ParishionerCollection


def parishioners_from_gsheet(session, extract_from_detailed_ledger):
    parishioner_gsheet = get_gsheet_fields(
        Parishioner,
        {
            'reference no': 'ID',
            'surname': 'SURNAME',
            'first name': 'FIRST_NAME',
            'title': 'TITLE',
            'spouse': 'SPOUSE',
            'address1': 'ADDRESS1',
            'address2': 'ADDRESS2',
            'address3': 'ADDRESS3',
            'county': 'County',
            'eircode': 'EIRCODE',
            'child1': 'CHILD_1',
            'dob1': 'DOB1',
            'child2': 'CHILD_2',
            'dob2': 'DOB2',
            'child3': 'CHILD_3',
            'dob3': 'DOB3',
            'child4': 'child 4',
            'dob4': 'DOB 4',
            'telephone': 'TELEPHONE',
            'giving': 'GIVING',
            'email': 'email',
        }
    )
    parishioner_mapping = Mapping(parishioner_gsheet, Parishioner.constructor_parameters)
    parishioners = extract_from_detailed_ledger(
        'parishioners',
        'A1',
        ('ID', 'SURNAME', 'FIRST_NAME', 'TITLE', 'SPOUSE', 'ADDRESS1', 'ADDRESS2', 'ADDRESS3', 'County', 'EIRCODE', 'CHILD_1', 'DOB1', 'CHILD_2', 'DOB2', 'CHILD_3', 'DOB3', 'child 4', 'DOB 4', 'TELEPHONE', 'GIVING', 'email')
    )
    load_class(session, parishioners, parishioner_mapping, Parishioner)