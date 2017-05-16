__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from sqlalchemy import Enum
from unittest.mock import Mock

from a_tuin.db import TableMap, PagedQuery
from a_tuin.db import DB_COLUMN_TYPE_MAP

from a_tuin.unittests.api.fixtures.models import (
    AClassStatus,
    AClassStatusField,
    AClass,
    AClassCollection,
    AReferringClass,
    AReferringClassCollection
)


DB_COLUMN_TYPE_MAP[AClassStatusField] = Enum(AClassStatus)

MOCK_SESSION = Mock()


def with_session(fn):
    def wrapped_with_session(self, args, context, info):
        return fn(self, args, context, info, MOCK_SESSION)

    return wrapped_with_session


TableMap(AClass, 'aclass', DB_COLUMN_TYPE_MAP)


class AClassQuery(PagedQuery):
    def __init__(self, session):
        super().__init__(AClass, AClassCollection, session)


TableMap(AReferringClass, 'areferringclass', DB_COLUMN_TYPE_MAP)


class AReferringClassQuery(PagedQuery):
    def __init__(self, session):
        super().__init__(AReferringClass, AReferringClassCollection, session)
