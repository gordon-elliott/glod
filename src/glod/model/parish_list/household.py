__copyright__ = 'Copyright(c) Gordon Elliott 2019'

""" 
id	ADDRESS1	ADDRESS2	ADDRESS3	County	EIRCODE	landline
"""


from a_tuin.metadata import StringField, ObjectFieldGroupBase, Collection, IntField


class Household(ObjectFieldGroupBase):
    # Receives household records from parish list

    public_interface = (
        IntField('reference_no', is_mutable=False),
        StringField('address1', required=True),
        StringField('address2'),
        StringField('address3'),
        StringField('county'),
        StringField('eircode'),
        StringField('telephone'),
    )


class HouseholdCollection(Collection):
    pass
