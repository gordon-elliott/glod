__copyright__ = 'Copyright(c) Gordon Elliott 2019'

""" 
"""

from a_tuin.metadata import (
    ObjectFieldGroupBase, Collection, ObjectReferenceField, BooleanField, DateTimeField
)


class CommunicationPermission(ObjectFieldGroupBase):

    # Flags indicating a persons communication preferences

    public_interface = (
        ObjectReferenceField('person', required=True),
        DateTimeField('gdpr_response'),
        BooleanField('by_email'),
        BooleanField('by_phone'),
        BooleanField('by_post'),
        BooleanField('news'),
        BooleanField('finance'),
    )

    def __str__(self):
        return '{0.__class__.__name__}({0._gdpr_response})'.format(self)


class CommunicationPermissionCollection(Collection):
    pass
