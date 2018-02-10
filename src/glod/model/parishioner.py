__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

from a_tuin.metadata import IntField, StringField, ObjectFieldGroupBase, Collection


class Parishioner(ObjectFieldGroupBase):
    # Data usage
    #
    # Denormalised data which is the initial representation of parishioner
    # contact information
    #

    public_interface = (
        IntField('reference_no', is_mutable=False),
        StringField('surname'),
        StringField('first_name'),
        StringField('title'),
        StringField('spouse'),
        StringField('status'),
        StringField('address1'),
        StringField('address2'),
        StringField('address3'),
        StringField('county'),
        StringField('eircode'),
        StringField('telephone'),
        StringField('child1'),
        StringField('dob1'),
        StringField('child2'),
        StringField('dob2'),
        StringField('child3'),
        StringField('dob3'),
        StringField('child4'),
        StringField('dob4'),
        StringField('giving'),
        StringField('email'),
    )

    @property
    def name(self):
        if self._spouse:
            return '{}, {} & {}'.format(self._surname, self._first_name, self._spouse)
        else:
            return '{}, {}'.format(self._surname, self._first_name)


class ParishionerCollection(Collection):
    pass
