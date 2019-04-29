__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.io.gsheet_integration import load_class
from a_tuin.metadata import Mapping, IntField, ListFieldGroup, UnusedField

from glod.db.envelope import Envelope
from glod.db.person import PersonQuery
from glod.db.counterparty import CounterpartyQuery


def envelopes_from_gsheet(session, extract_from_detailed_ledger):

    gs_field_year = IntField('year')
    gs_field_counterparty = IntField('counterpartyid')
    gs_field_parishioner = IntField('parishionerid')
    gs_field_envelope_number = IntField('envelope number')

    envelope_gsheet = ListFieldGroup(
        (
            gs_field_year,
            gs_field_counterparty,
            gs_field_parishioner,
            UnusedField('household id'),
            gs_field_envelope_number,
        )
    )

    field_mappings = tuple(zip(
        (
            gs_field_year,
            gs_field_counterparty,
            gs_field_parishioner,
            gs_field_envelope_number,
        ),
        Envelope.constructor_parameters
    ))

    field_casts = {
        'counterpartyid': CounterpartyQuery(session).instance_finder('reference_no', int),
        'parishionerid': PersonQuery(session).instance_finder('parishioner_reference_no', int),
    }
    envelope_mapping = Mapping(envelope_gsheet, Envelope.constructor_parameters, field_mappings, field_casts)
    envelopes = extract_from_detailed_ledger(
        'FWE records',
        'A1',
        ('year', 'counterpartyid', 'parishionerid', 'household id', 'envelope number')
    )
    load_class(session, envelopes, envelope_mapping, Envelope)
