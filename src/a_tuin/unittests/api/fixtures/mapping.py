__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from sqlalchemy import Enum
from unittest.mock import Mock

from a_tuin.db import TableMap, PagedQuery, RelationMap
from a_tuin.db import DB_COLUMN_TYPE_MAP

from a_tuin.unittests.api.fixtures.models import (
    AClassStatus,
    AClassStatusField,
    AClass,
    AClassCollection,
    AReferringClass,
    AReferringClassCollection,
    areferringclass__aclass
)


DB_COLUMN_TYPE_MAP[AClassStatusField] = Enum(AClassStatus)
SCHEMA_NAME = 'a_schema'

MOCK_SESSION = Mock()


def with_session(fn):
    def wrapped_with_session(self, info, **kwargs):
        context = info.context
        return fn(self, kwargs, context, info, MOCK_SESSION)

    return wrapped_with_session


TableMap(AClass, SCHEMA_NAME, 'aclass', DB_COLUMN_TYPE_MAP)


class AClassQuery(PagedQuery):
    def __init__(self, session):
        super().__init__(AClass, AClassCollection, session)


TableMap(AReferringClass, SCHEMA_NAME, 'areferringclass', DB_COLUMN_TYPE_MAP,
    RelationMap(areferringclass__aclass, 'aclass._id'))


class AReferringClassQuery(PagedQuery):
    def __init__(self, session):
        super().__init__(AReferringClass, AReferringClassCollection, session)
