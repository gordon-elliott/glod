__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""


from a_tuin.metadata import (
    ObjectFieldGroupBase,
    StringField,
    ObjectReferenceField,
    Collection,
)


class PPS(ObjectFieldGroupBase):

    public_interface = (
        ObjectReferenceField('person'),
        StringField('pps'),
    )


class PPSCollection(Collection):
    pass
