from a_tuin.metadata.reference import Reference

__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from enum import IntEnum

from a_tuin.metadata import (
    Collection,
    ObjectFieldGroupBase,
    StringField,
    DateField,
    IntField,
    BooleanField,
    IntEnumField,
    ObjectReferenceField,
)
from a_tuin.metadata.reference import REFERENCES


class AClassStatus(IntEnum):
    Open = 1
    Closed = 2


class AClassStatusField(IntEnumField):
    def __init__(self, name, is_mutable=True, required=False, default=None, description=None, validation=None):
        super().__init__(name, AClassStatus, is_mutable, required, default, description, validation)


class AClass(ObjectFieldGroupBase):
    public_interface = (
        IntField('ref_no'),
        StringField('name'),
        BooleanField('is_running'),
        AClassStatusField('status'),
        DateField('date'),
    )


class AClassCollection(Collection):
    pass


class AReferringClass(ObjectFieldGroupBase):
    public_interface = (
        StringField('name'),
        ObjectReferenceField('aclass'),
    )


class AReferringClassCollection(Collection):
    pass


areferringclass__aclass = Reference(AReferringClass, 'aclass', AClass)

REFERENCES.extend((
    areferringclass__aclass,
))


class ATypedClass(ObjectFieldGroupBase):
    public_interface = (
        StringField('name'),
        IntField('type'),
    )


class ATypedClassCollection(Collection):
    pass
