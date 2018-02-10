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

    # May be a degenerate object which just refers to an Organisation

    public_interface = (
        ObjectReferenceField('organisation', required=True),
        StringField('family_name', description='Surname of individual. Used to correctly address communications to them.'),
        StringField('given_name', description='First name of individual. Used to correctly address communications to them.'),
        PersonStatusField('status', required=True, default=PersonStatus.Active, description='Is the person living, deceased or has contact been lost with them.'),
        StringField('title', description='Honorific used in formal communications and when addressing letters.'),
        StringField('mobile', description='In addition to facilitating voice communications may be used to supplement secure access to personal data.'),
        StringField('email', description='Primary means of electronic communication and identity for maintaining personal information.'),
        DateField('date_of_birth', description='Optional information for adults. Used to identify minors.'),
        BooleanField('dob_is_estimate', description='Flag indicating whether date of birth has been verified by family member.'),
        IntField('parishioner_reference_no', is_mutable=False, description='Internal use. Refers to identity in source data. Required for initial data load.'),
    )

    def __str__(self):
        return '{0.__class__.__name__}({0._parishioner_reference_no}, {0.name})'.format(self)

    @property
    def name(self):
        if self._title:
            return '{0._title} {0._given_name} {0._family_name}'.format(self)
        else:
            return '{0._given_name} {0._family_name}'.format(self)


class PersonCollection(Collection):
    pass
