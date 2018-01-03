__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from unittest import TestCase

from glod.model.organisation import Organisation, OrganisationType, OrganisationStatus
from glod.model.address import Address
from glod.model.organisation_address import OrganisationAddress, OrganisationAddressStatus
from glod.model.person import Person, PersonStatus


class TestOrganisation(TestCase):

    def test_household(self):

        household = Organisation(1490, 'Jones', OrganisationType.Household)
        parent0 = Person(household, 'Jones', 'Joe', title='Ms', mobile='9383938', email='joe@jones.ie')
        parent1 = Person(household, 'Grant', 'Bob', title='Ms', mobile='220938', email='bob@grant.le')
        kid0 = Person(household, 'Jones-Grant', 'Alfie')
        kid1 = Person(household, 'Jones-Grant', 'Bertie')
        kid2 = Person(household, 'Jones-Grant', 'Callie')

        home = Address('2, Main St', 'Newtown', '', 'Wicklow', 'IE', 'A63 D444', '39389288')
        oa_link = OrganisationAddress(household, home, OrganisationAddressStatus.Current)

        for person in (parent0, parent1, kid0, kid1, kid2):
            self.assertEqual(PersonStatus.Active, person._status)
