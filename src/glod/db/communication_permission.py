__copyright__ = 'Copyright(c) Gordon Elliott 2019'

""" 
"""

from a_tuin.db import TableMap, PagedQuery, InstanceQuery, RelationMap

from glod.model.communication_permission import CommunicationPermission, CommunicationPermissionCollection
from glod.model.references import communication_permission__person

from glod.db.db_column_type_map import DB_COLUMN_TYPE_MAP


TableMap(
    CommunicationPermission,
    'communication_permission',
    DB_COLUMN_TYPE_MAP,
    RelationMap(
        communication_permission__person,
        'person._id',
        backref='communication_permissions',
        lazy='selectin'
    ),)


class CommunicationPermissionInstanceQuery(InstanceQuery):
    def __init__(self, session):
        super().__init__(CommunicationPermission, CommunicationPermissionCollection, session)


class CommunicationPermissionQuery(PagedQuery):
    def __init__(self, session):
        super().__init__(CommunicationPermission, CommunicationPermissionCollection, session)
