__copyright__ = 'Copyright(c) Gordon Elliott 2019'

""" 
"""

from glod.model.address import Address


def _reorganise_household(household):

    address = Address(
        household.address1,
        household.address2,
        household.address3,
        household.county,
        'IE',
        household.eircode,
        household.telephone
    )
    return household.reference_no, address


def reorganise_households(session, households):

    new_entities = dict(
        _reorganise_household(household)
        for household in households
    )
    session.add_all(new_entities.values())
    return new_entities
