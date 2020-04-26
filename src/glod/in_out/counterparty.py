__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""
from a_tuin.metadata import IntField, StringField, UnusedField, ListFieldGroup, Mapping
from a_tuin.in_out.gsheet_integration import load_class
from glod.db.counterparty import Counterparty
from glod.db.person import PersonQuery
from glod.db import OrganisationQuery


def cast_yes_no(value, _):
    return value.lower() == 'yes'


def counterparty_from_gsheet(session, extract_from_detailed_ledger):

    gs_field_id = IntField('id')
    gs_field_bank_text = StringField('bank text')
    gs_field_person = IntField('parishoner id')
    gs_field_organisation = IntField('household id')
    gs_field_name_override = StringField('name override')
    gs_field_method = StringField('method')
    gs_field_so_card = StringField('SO card?')
    gs_field_by_email = StringField('by email')
    gs_field_notes = StringField('notes')

    counterparty_gsheet = ListFieldGroup(
        (
            gs_field_id,
            gs_field_bank_text,
            gs_field_person,
            gs_field_organisation,
            UnusedField('main contact'),
            UnusedField('.'),
            gs_field_name_override,
            UnusedField('name'),
            UnusedField('_'),
            UnusedField('reverse lookup parishoner id'),
            UnusedField('reverse lookup cp id'),
            UnusedField('__'),
            UnusedField('___'),
            UnusedField('____'),
            UnusedField('_____'),
            UnusedField('______'),
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
            gs_field_person,
            gs_field_organisation,
            gs_field_name_override,
            gs_field_method,
            gs_field_so_card,
            gs_field_by_email,
            gs_field_notes,
        ),
        Counterparty.constructor_parameters
    ))

    field_casts = {
        'parishoner id': PersonQuery(session).instance_finder('parishioner_reference_no', int),
        'household id': OrganisationQuery(session).instance_finder('reference_no', int),
        'SO card?': cast_yes_no,
        'by email': cast_yes_no,
    }

    counterparty_mapping = Mapping(counterparty_gsheet, Counterparty.constructor_parameters, field_mappings, field_casts)
    counterparties = extract_from_detailed_ledger(
        'counterparties',
        'A1',
        (
            'id', 'bank text', 'parishoner id', 'household id', 'main contact', '.', 'name override',
            'name', '_', 'reverse lookup parishoner id', 'reverse lookup cp id',
            '__', '___', '____', '_____', '______', 'method', 'SO card?', 'by email', 'notes'
        )
    )
    load_class(session, counterparties, counterparty_mapping, Counterparty)
