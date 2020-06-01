__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from enum import IntEnum

from a_tuin.metadata import (
    ObjectFieldGroupBase,
    StringField,
    ObjectReferenceField,
    Collection,
    DescriptionField,
    IntField,
    IntEnumField,
)


class PPSStatus(IntEnum):
    Requested = 1
    Provided = 2
    NotIncomeTaxPayer = 3   # parishioner is not an Irish income tax payer
    NotProvided = 4         # parishioner responded but refused to provide PPS
    ExcludedByAdmin = 5     # parishioner excluded  through admin discretion


class PPSStatusField(IntEnumField):
    def __init__(self, name, is_mutable=True, required=False, default=None, description=None, validation=None):
        super().__init__(name, PPSStatus, is_mutable, required, default, description, validation)


class PPS(ObjectFieldGroupBase):
    # Data usage
    #
    # Records PPS number for an individual in order that a tax rebate may be claimed
    # on funds donated to the parish.

    public_interface = (
        ObjectReferenceField('person', required=True),
        PPSStatusField(
            'status',
            required=True,
            default=PPSStatus.Requested,
            description='Has the parishioner responded to a request for a PPS?'
        ),
        StringField('pps'),
        StringField('name_override'),
        IntField('chy3_valid_year', description='The first financial year the most recent CHY3 form is valid from'),
        DescriptionField('notes')
    )


class PPSCollection(Collection):
    pass
