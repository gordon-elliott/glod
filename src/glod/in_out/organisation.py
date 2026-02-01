__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import logging
from datetime import datetime

from glod.model.communication_permission import CommunicationPermission
from glod.model.organisation import Organisation, OrganisationCategory, OrganisationStatus
from glod.model.organisation_address import OrganisationAddress
from glod.model.person import Person

LOG = logging.getLogger(__file__)

INITIAL_GDPR_SURVEY = datetime(2018, 10, 30)
TRUE_STRINGS = ("true", "True", "TRUE", "yes", "Yes", "YES", "1")
IS_PRIMARY = 'primary'


def _reorganise_parishioner(parishioner, address_map, household_map):
    new_entities = []
    parishioner_status = parishioner.status.lower()
    if parishioner_status == 'foreign list':
        organisation_status = OrganisationStatus.Active
        organisation_category = OrganisationCategory.NonLocalHousehold
    else:
        organisation_status = OrganisationStatus.Active if parishioner_status == 'active' else OrganisationStatus.Inactive
        organisation_category = OrganisationCategory.Household
    household_ref_no = parishioner.household_ref_no
    if household_ref_no in household_map:
        household = household_map[household_ref_no]
    else:
        household = Organisation(
            parishioner.surname,
            organisation_category,
            organisation_status,
            household_ref_no,
        )
        address = address_map[household_ref_no]
        oa_link = OrganisationAddress(household, address)
        household_map[household_ref_no] = household
        new_entities = [household, oa_link]

    person = Person(
        household,
        parishioner.surname,
        parishioner.first_name,
        title=parishioner.title,
        mobile=parishioner.mobile,
        other_phone=parishioner.other,
        email=parishioner.email,
        parishioner_reference_no=parishioner.reference_no,
    )
    communication_preferences = CommunicationPermission(
        person,
        parishioner.main_contact == IS_PRIMARY,
        INITIAL_GDPR_SURVEY,
        parishioner.by_email in TRUE_STRINGS,
        parishioner.by_phone in TRUE_STRINGS,
        parishioner.by_post in TRUE_STRINGS,
        parishioner.news in TRUE_STRINGS,
        parishioner.finance in TRUE_STRINGS,
    )
    new_entities += [person, communication_preferences]
    return new_entities


def reorganise_parishioners(session, parishioners, address_map):

    household_map = {}
    for parishioner in parishioners:
        new_entities = _reorganise_parishioner(parishioner, address_map, household_map)

        session.add_all(new_entities)
