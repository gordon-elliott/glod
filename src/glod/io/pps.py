__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.io.gsheet_integration import load_class
from a_tuin.metadata import Mapping, StringField, IntField, UnusedField, ListFieldGroup

from glod.db.pps import PPS
from glod.db.person import PersonQuery


def ppses_from_gsheet(session, extract_from_detailed_ledger):

    gs_field_parishioner_id = IntField('parishioner id')
    gs_field_pps = StringField('pps')
    gs_field_name_override = StringField('tax payer name override')
    gs_field_notes = StringField('notes')

    pps_gsheet = ListFieldGroup(
        (
            gs_field_parishioner_id,
            gs_field_pps,
            UnusedField('is valid'),
            gs_field_name_override,
            UnusedField('tax payer name'),
            gs_field_notes,
        )
    )

    field_mappings = tuple(zip(
        (
            gs_field_parishioner_id,
            gs_field_pps,
            gs_field_name_override,
            gs_field_notes,
        ),
        PPS.constructor_parameters
    ))

    field_casts = {
        'parishioner id': PersonQuery(session).instance_finder('parishioner_reference_no', int),
    }
    pps_mapping = Mapping(pps_gsheet, PPS.constructor_parameters, field_mappings, field_casts)
    ppses = extract_from_detailed_ledger(
        'pps',
        'C1',
        ('parishioner id', 'pps', 'is valid', 'tax payer name override', 'tax payer name', 'notes')
    )
    load_class(session, ppses, pps_mapping, PPS)
