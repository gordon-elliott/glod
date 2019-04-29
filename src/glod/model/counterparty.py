__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""
from a_tuin.metadata import (
    ObjectReferenceField,
    StringField,
    IntField,
    BooleanField,
    ObjectFieldGroupBase,
    Collection,
    DescriptionField
)


class Counterparty(ObjectFieldGroupBase):
    # Data usage
    #
    # Associates an identifiable person with their financial activity
    #

    public_interface = (
        IntField('reference_no'),
        StringField('bank_text', description='Used to identify donors from bank statements'),
        ObjectReferenceField('person'),
        ObjectReferenceField('organisation'),
        StringField('name_override'),
        StringField('method', description='Method whereby funds are received or dispersed. Used to aid reconciliation.'),          # TODO enum?
        BooleanField('has_SO_card', description='Has donor requested a standing order donor card.'),
        BooleanField('by_email', 'Has the donor agreed to receive communications by email?'),
        DescriptionField('notes', 'Free text record of unusual circumstances.'),
    )

    def __str__(self):
        return '{0.__class__.__name__}({0._reference_no}, {0.name}, {0._bank_text})'.format(self)

    @property
    def name(self):
        return self._name_override if self._name_override else self._person.name

    @property
    def lookup_name(self):
        return self.name.lower()


class CounterpartyCollection(Collection):
    pass
