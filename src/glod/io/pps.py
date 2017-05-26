__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.io.gsheet_integration import get_gsheet_fields, load_class
from a_tuin.metadata import Mapping, StringField

from glod.db.pps import PPS
from glod.db.parishioner import ParishionerQuery


def ppses_from_gsheet(session, extract_from_detailed_ledger):

    pps_gsheet = get_gsheet_fields(
        PPS,
        {'parishioner': 'parishioner id'}
    )
    pps_gsheet['parishioner id'] = StringField('parishioner id')
    field_casts = {
        'parishioner id': ParishionerQuery(session).instance_finder('reference_no', int),
    }
    pps_mapping = Mapping(pps_gsheet, PPS.constructor_parameters, field_casts=field_casts)
    ppses = extract_from_detailed_ledger(
        'pps',
        'B1',
        ('parishioner id', 'pps')
    )
    ppses = list(ppses)
    load_class(session, ppses, pps_mapping, PPS)
