__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from enum import IntEnum

from a_tuin.metadata import StringField, ObjectFieldGroupBase, Collection, ObjectReferenceField, IntEnumField


class OrganisationAddressStatus(IntEnum):
    Current = 1
    Prior = 2


class OrganisationAddressStatusField(IntEnumField):
    def __init__(self, name, is_mutable=True, required=False, default=None, description=None, validation=None):
        super().__init__(name, OrganisationAddressStatus, is_mutable, required, default, description, validation)


class OrganisationAddress(ObjectFieldGroupBase):
    # Data usage
    #
    # Allows addresses to be associated with an organisation
    #

    public_interface = (
        ObjectReferenceField('organisation', required=True),
        ObjectReferenceField('address', required=True),
        OrganisationAddressStatusField('status', required=True, default=OrganisationAddressStatus.Current),
    )


class OrganisationAddressCollection(Collection):
    pass
