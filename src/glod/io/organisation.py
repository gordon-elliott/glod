__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import logging

from datetime import datetime, date, timedelta

from glod.db.address import Address
from glod.db.person import Person
from glod.db.organisation import Organisation, OrganisationCategory, OrganisationStatus
from glod.db.organisation_address import OrganisationAddress


LOG = logging.getLogger(__file__)

AMPERSAND = ' & '
BASE_DATE_1899 = date(1899, 11, 30)
FUTURE_DATE = date.today() + timedelta(days=365*3)

PHONE_SPLIT_CHAR = ';'
MOBILE_PREFIX = '08'


def _parse_inconsistent_birth_date(date_string):
    try:
        from_string = datetime.strptime(date_string, '%d/%m/%Y').date()
    except ValueError:
        num_chars = len(date_string)
        if num_chars==6:
            try:
                from_string = datetime.strptime(date_string, '%y%m%d').date()
            except ValueError:
                from_string = None
        elif num_chars==5:
            try:
                since_1899 = int(date_string)
                from_string = BASE_DATE_1899 + timedelta(days=since_1899)
            except ValueError:
                from_string = None
        else:
            from_string = None
    if from_string and from_string > FUTURE_DATE:
        LOG.error('Unable to find a reasonable birth date from {}'.format(date_string))
        from_string = None
    return from_string


def _child_data(parishioner):
    for i in range(1, 5):
        name_field = 'child{}'.format(i)
        dob_field = 'dob{}'.format(i)
        name = getattr(parishioner, name_field)
        dob_string = getattr(parishioner, dob_field)
        dob = _parse_inconsistent_birth_date(dob_string) if dob_string else None
        if name:
            yield name, dob


def _assign_mobiles(number, main_mobile, other_mobile):
    if main_mobile is None:
        main_mobile = number
    elif other_mobile is None:
        other_mobile = number
    return main_mobile, other_mobile


def _parse_phone_numbers(parishioner):
    landline, main_mobile, other_mobile = None, None, None
    phone_string = parishioner.telephone
    if phone_string:
        for number in phone_string.split(PHONE_SPLIT_CHAR):
            number = number.strip()
            if number.startswith(MOBILE_PREFIX):
                main_mobile, other_mobile = _assign_mobiles(number, main_mobile, other_mobile)
            else:
                if landline is None:
                    landline = number
                else:
                    main_mobile, other_mobile = _assign_mobiles(number, main_mobile, other_mobile)

    return landline, main_mobile, other_mobile


def _reorganise_parishioner(parishioner, address_map):
    parishioner_status = parishioner.status.lower()
    if parishioner_status == 'foreign list':
        organisation_status = OrganisationStatus.Active
        organisation_category = OrganisationCategory.NonLocalHousehold
    else:
        organisation_status = OrganisationStatus.Active if parishioner_status == 'active' else OrganisationStatus.Inactive
        organisation_category = OrganisationCategory.Household
    household = Organisation(
        parishioner.reference_no,
        parishioner.surname,
        organisation_category,
        organisation_status,
    )
    landline, main_mobile, other_mobile = _parse_phone_numbers(parishioner)
    main_contact = Person(
        household,
        parishioner.surname,
        parishioner.first_name,
        title=parishioner.title,
        mobile=main_mobile,
        email=parishioner.email,
        parishioner_reference_no=parishioner.reference_no,
    )
    new_entities = [household, main_contact]
    address = address_map[parishioner.household_ref_no]
    new_entities.append(address)
    oa_link = OrganisationAddress(household, address)
    new_entities.append(oa_link)
    return new_entities


def reorganise_parishioners(session, parishioners, address_map):

    for parishioner in parishioners:
        new_entities = _reorganise_parishioner(parishioner, address_map)

        session.add_all(new_entities)
