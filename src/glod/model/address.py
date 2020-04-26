__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.metadata import StringField, ObjectFieldGroupBase, Collection


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


class AddressCollection(Collection):
    pass
