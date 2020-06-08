__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.metadata import StringField, ObjectFieldGroupBase, Collection

COUNTRY_ISO_LOOKUP = {
    'GB': 'UK',
}


class Address(ObjectFieldGroupBase):
    # Data usage
    #
    # 1. delivering messages by postal system
    # 2. arranging house visits
    #

    public_interface = (
        StringField('address1', required=True),
        StringField('address2'),
        StringField('address3'),
        StringField('county'),
        StringField('countryISO', required=True),
        StringField('eircode'),
        StringField('telephone'),
    )

    def post_label(self, addressees=None):

        address_1 = self.address1
        address_2 = self.address2
        if address_1 and address_2 and len(address_1) <= 3:     # it's most likely a house number
            address_2 = f"{address_1}, {address_2}"
            address_1 = None

        label_fields = filter(
            lambda a: a,    # drop None and empty strings
            (
                addressees,
                address_1,
                address_2,
                self.address3,
                self.county,
                self.eircode,
                COUNTRY_ISO_LOOKUP.get(self.countryISO)
            )
        )
        return ",\n".join(label_fields)


class AddressCollection(Collection):
    pass
