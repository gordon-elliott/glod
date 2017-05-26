__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""
from enum import IntEnum

from a_tuin.metadata import (
    ObjectReferenceField,
    StringField,
    IntField,
    IntEnumField,
    BooleanField,
    ObjectFieldGroupBase,
    Collection,
)


class StandingOrderDonor(IntEnum):
    Yes = 1
    No = 2
    Monthly = 3
    Quarterly = 4
    Other = 5


class StandingOrderDonorField(IntEnumField):
    def __init__(self, name, is_mutable=True, required=False, default=None, description=None, validation=None):
        super().__init__(name, StandingOrderDonor, is_mutable, required, default, description, validation)


class Counterparty(ObjectFieldGroupBase):

    public_interface = (
        IntField('reference_no'),
        StringField('bank_text'),
        ObjectReferenceField('parishioner'),
        StringField('name_override'),
        StandingOrderDonorField('standing_order_donor'),
        StringField('sustentation'),    # TODO enum?
        StringField('method'),          # TODO enum?
        BooleanField('has_SO_card'),
        StringField('notes'),
    )

    @property
    def name(self):
        return self._name_override if self._name_override else self._parishioner.name


class CounterpartyCollection(Collection):
    pass
