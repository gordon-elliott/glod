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
    # Data usage
    #
    # Records PPS number for an individual in order that a tax rebate may be claimed
    # on funds donated to the parish.


    public_interface = (
        ObjectReferenceField('person'),
        StringField('pps'),
    )


class PPSCollection(Collection):
    pass
