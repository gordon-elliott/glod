__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

from a_tuin.metadata import IntField, StringField, ArgsFieldGroup, ObjectFieldGroupMeta


class Parishioner(object, metaclass=ObjectFieldGroupMeta):

    constructor_parameters = ArgsFieldGroup(
        (
            IntField('reference_no'),
            StringField('surname'),
            StringField('first_name'),
            StringField('title'),
            StringField('spouse'),
            StringField('address1'),
            StringField('address2'),
            StringField('address3'),
            StringField('county'),
            StringField('eircode'),
            StringField('child1'),
            StringField('dob1'),
            StringField('child2'),
            StringField('dob2'),
            StringField('child3'),
            StringField('dob3'),
            StringField('child4'),
            StringField('dob4'),
            StringField('telephone'),
            StringField('giving'),
            StringField('email'),
        )
    )

    # metaclass takes care of dealing with the args
    def __init__(self, *args, **kwargs):
        pass

    @property
    def id(self):
        return self._id

    @property
    def reference_no(self):
        return self._reference_no

    @reference_no.setter
    def reference_no(self, value):
        self._reference_no = value

    @property
    def surname(self):
        return self._surname

    @surname.setter
    def surname(self, value):
        self._surname = value

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def spouse(self):
        return self._spouse

    @spouse.setter
    def spouse(self, value):
        self._spouse = value

    @property
    def address1(self):
        return self._address1

    @address1.setter
    def address1(self, value):
        self._address1 = value

    @property
    def address2(self):
        return self._address2

    @address2.setter
    def address2(self, value):
        self._address2 = value

    @property
    def address3(self):
        return self._address3

    @address3.setter
    def address3(self, value):
        self._address3 = value

    @property
    def county(self):
        return self._county

    @county.setter
    def county(self, value):
        self._county = value

    @property
    def eircode(self):
        return self._eircode

    @eircode.setter
    def eircode(self, value):
        self._eircode = value

    @property
    def child1(self):
        return self._child1

    @child1.setter
    def child1(self, value):
        self._child1 = value

    @property
    def dob1(self):
        return self._dob1

    @dob1.setter
    def dob1(self, value):
        self._dob1 = value

    @property
    def child2(self):
        return self._child2

    @child2.setter
    def child2(self, value):
        self._child2 = value

    @property
    def dob2(self):
        return self._dob2

    @dob2.setter
    def dob2(self, value):
        self._dob2 = value

    @property
    def child3(self):
        return self._child3

    @child3.setter
    def child3(self, value):
        self._child3 = value

    @property
    def dob3(self):
        return self._dob3

    @dob3.setter
    def dob3(self, value):
        self._dob3 = value

    @property
    def child4(self):
        return self._child4

    @child4.setter
    def child4(self, value):
        self._child4 = value

    @property
    def dob4(self):
        return self._dob4

    @dob4.setter
    def dob4(self, value):
        self._dob4 = value

    @property
    def telephone(self):
        return self._telephone

    @telephone.setter
    def telephone(self, value):
        self._telephone = value

    @property
    def giving(self):
        return self._giving

    @giving.setter
    def giving(self, value):
        self._giving = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value
