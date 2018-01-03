__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from enum import IntEnum

from a_tuin.metadata import (
    StringField, ObjectFieldGroupBase, Collection, ObjectReferenceField, IntEnumField,
    DateField, BooleanField, IntField
)


class PersonStatus(IntEnum):
    Active = 1
    LostContact = 2
    Deceased = 3


class PersonStatusField(IntEnumField):
    def __init__(self, name, is_mutable=True, required=False, default=None, description=None, validation=None):
        super().__init__(name, PersonStatus, is_mutable, required, default, description, validation)


class Person(ObjectFieldGroupBase):

    public_interface = (
        ObjectReferenceField('organisation', required=True),
        StringField('family_name', required=True),
        StringField('given_name', required=True),
        PersonStatusField('status', required=True, default=PersonStatus.Active),
        StringField('title'),
        StringField('mobile'),
        StringField('email'),
        DateField('date_of_birth'),
        BooleanField('dob_is_estimate'),
        IntField('parishioner_reference_no', is_mutable=False),
    )


class PersonCollection(Collection):
    pass
