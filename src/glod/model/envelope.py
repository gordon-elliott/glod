__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.metadata import (
    ObjectFieldGroupBase,
    IntField,
    ObjectReferenceField,
    Collection,
)


class Envelope(ObjectFieldGroupBase):
    # Data usage
    #
    # Used to administer the Free-will envelope programme.
    # Records the envelope used by a person in a particular year
    #

    public_interface = (
        IntField('year'),
        ObjectReferenceField('counterparty'),
        ObjectReferenceField('person'),
        IntField('envelope_number'),
    )


class EnvelopeCollection(Collection):
    pass
