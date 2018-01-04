__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""


from enum import IntEnum

from a_tuin.metadata import StringField, ObjectFieldGroupBase, Collection, IntEnumField, IntField


class OrganisationCategory(IntEnum):
    Household = 1
    NonLocalHousehold = 2
    Company = 3
    Charity = 4
    Government = 5


class OrganisationCategoryField(IntEnumField):
    def __init__(self, name, is_mutable=True, required=False, default=None, description=None, validation=None):
        super().__init__(name, OrganisationCategory, is_mutable, required, default, description, validation)


class OrganisationStatus(IntEnum):
    Active = 1
    Inactive = 2


class OrganisationStatusField(IntEnumField):
    def __init__(self, name, is_mutable=True, required=False, default=None, description=None, validation=None):
        super().__init__(name, OrganisationStatus, is_mutable, required, default, description, validation)


class Organisation(ObjectFieldGroupBase):

    public_interface = (
        IntField('reference_no', required=True, is_mutable=False),
        StringField('name', required=True),
        OrganisationCategoryField('category', required=True),
        OrganisationStatusField('status', required=True, default=OrganisationStatus.Active),
    )


class OrganisationCollection(Collection):
    pass
