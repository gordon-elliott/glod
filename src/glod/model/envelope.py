__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.metadata import (
    ObjectFieldGroupBase,
    IntField,
    ObjectReferenceField,
)


class Envelope(ObjectFieldGroupBase):

    public_interface = (
        IntField('year'),
        ObjectReferenceField('counterparty'),
        ObjectReferenceField('parishioner'),
        IntField('envelope_number'),
    )
