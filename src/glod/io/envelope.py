__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.io.gsheet_integration import get_gsheet_fields, load_class
from a_tuin.metadata import Mapping

from glod.db.envelope import Envelope
from glod.db.person import PersonQuery
from glod.db.counterparty import CounterpartyQuery


def envelopes_from_gsheet(session, extract_from_detailed_ledger):

    envelope_gsheet = get_gsheet_fields(
        Envelope,
        {'counterparty': 'counterpartyid', 'person': 'parishionerid'}
    )
    field_casts = {
        'counterpartyid': CounterpartyQuery(session).instance_finder('reference_no', int),
        'parishionerid': PersonQuery(session).instance_finder('parishioner_reference_no', int),
    }
    envelope_mapping = Mapping(envelope_gsheet, Envelope.constructor_parameters, field_casts=field_casts)
    envelopes = extract_from_detailed_ledger(
        'FWE records',
        'A1',
        ('year', 'counterpartyid', 'parishionerid', 'envelope number')
    )
    load_class(session, envelopes, envelope_mapping, Envelope)
