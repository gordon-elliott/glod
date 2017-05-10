__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from enum import IntEnum

from a_tuin.metadata import (
    Collection,
    ObjectFieldGroupBase,
    StringField,
    IntField,
    BooleanField,
    IntEnumField,
    ObjectReferenceField,
)


class AClassStatus(IntEnum):
    Open = 1
    Closed = 2


class AClassStatusField(IntEnumField):
    def __init__(self, name, is_mutable=True, required=False, default=None, description=None, validation=None):
        super().__init__(name, AClassStatus, is_mutable, required, default, description, validation)


class AClass(ObjectFieldGroupBase):
    public_interface = (
        IntField('refNo'),
        StringField('name'),
        BooleanField('isRunning'),
        AClassStatusField('status')
    )


class AClassCollection(Collection):
    pass


class AReferringClass(ObjectFieldGroupBase):
    public_interface = (
        (
            StringField('name'),
            ObjectReferenceField('aclass'),
        )
    )


class AReferringClassCollection(Collection):
    pass