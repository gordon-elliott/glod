__copyright__ = 'Copyright(c) Gordon Elliott 2019'

""" 
"""


from a_tuin.in_out.gsheet_integration import get_gsheet_fields, model_instances
from a_tuin.metadata import Mapping

from glod.db.parish_list.household import Household


def households_from_gsheet(session, extract_from_parish_list):
    household_gsheet = get_gsheet_fields(
        Household,
        {
            'reference no': 'id',
            'address1': 'ADDRESS1',
            'address2': 'ADDRESS2',
            'address3': 'ADDRESS3',
            'county': 'County',
            'eircode': 'EIRCODE',
            'telephone': 'landline',
        }
    )
    household_mapping = Mapping(household_gsheet, Household.constructor_parameters)
    household_rows = extract_from_parish_list(
        'households',
        'A1',
        ('id', 'ADDRESS1', 'ADDRESS2', 'ADDRESS3', 'County', 'EIRCODE', 'landline')
    )
    households = list(model_instances(household_rows, household_mapping, Household))
    session.add_all(households)
