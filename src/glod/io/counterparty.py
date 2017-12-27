__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""
from a_tuin.metadata import IntField, StringField, UnusedField, ListFieldGroup, Mapping
from a_tuin.io.gsheet_integration import load_class
from glod.db.counterparty import Counterparty, StandingOrderDonor
from glod.db.parishioner import ParishionerQuery


STANDING_ORDER_DONOR_MAP = {
    'yes': StandingOrderDonor.Yes,
    'no': StandingOrderDonor.No,
    'monthly': StandingOrderDonor.Monthly,
    'quarterly': StandingOrderDonor.Quarterly,
    'other': StandingOrderDonor.Other,
}


def cast_standing_order_donor(value, _):
    return STANDING_ORDER_DONOR_MAP.get(value.lower())


def cast_yes_no(value, _):
    return value.lower() == 'yes'


def counterparty_from_gsheet(session, extract_from_detailed_ledger):

    gs_field_id = IntField('id')
    gs_field_bank_text = StringField('bank text')
    gs_field_parishioner = IntField('parishoner id')
    gs_field_name_override = StringField('name override')
    gs_field_standing_order_donor = StringField('standing order donor')
    gs_field_sustentation = StringField('sustentation')
    gs_field_method = StringField('method')
    gs_field_so_card = StringField('SO card?')
    gs_field_by_email = StringField('by email')
    gs_field_notes = StringField('notes')

    counterparty_gsheet = ListFieldGroup(
        (
            gs_field_id,
            gs_field_bank_text,
            gs_field_parishioner,
            UnusedField('fwe number'),
            gs_field_name_override,
            UnusedField('name'),
            UnusedField('reverse lookup parishoner id'),
            UnusedField('reverse lookup cp id'),
            gs_field_standing_order_donor,
            UnusedField('is 2015 SO donor'),
            gs_field_sustentation,
            UnusedField('free will envelope'),
            UnusedField('foreign list'),
            gs_field_method,
            gs_field_so_card,
            gs_field_by_email,
            gs_field_notes,
        )
    )

    field_mappings = tuple(zip(
        (
            gs_field_id,
            gs_field_bank_text,
            gs_field_parishioner,
            gs_field_name_override,
            gs_field_standing_order_donor,
            gs_field_sustentation,
            gs_field_method,
            gs_field_so_card,
            gs_field_by_email,
            gs_field_notes,
        ),
        Counterparty.constructor_parameters
    ))

    field_casts = {
        'parishoner id': ParishionerQuery(session).instance_finder('reference_no', int),
        'standing order donor': cast_standing_order_donor,
        'SO card?': cast_yes_no,
        'by email': cast_yes_no,
    }

    counterparty_mapping = Mapping(counterparty_gsheet, Counterparty.constructor_parameters, field_mappings, field_casts)
    counterparties = extract_from_detailed_ledger(
        'counterparties',
        'A1',
        ('id', 'bank text', 'parishoner id', 'fwe number', 'name override', 'name', 'reverse lookup parishoner id', 'reverse lookup cp id', 'standing order donor', 'is 2015 SO donor', 'sustentation', 'free will envelope', 'foreign list', 'method', 'SO card?', 'by email', 'notes')
    )
    load_class(session, counterparties, counterparty_mapping, Counterparty)
