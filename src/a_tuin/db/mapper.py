__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""
from sqlalchemy import (
    String,
    Integer,
    Date,
    Numeric,
    Boolean
)

from a_tuin.metadata import (
    ObjectReferenceField,
    BooleanField,
    IntField,
    StringField,
    DateField,
    DecimalField,
)

REGULAR_STRING = String(64)
CURRENCY = Numeric(scale=2)

DB_COLUMN_TYPE_MAP = {
    ObjectReferenceField: Integer,
    BooleanField: Boolean,
    IntField: Integer,
    StringField: REGULAR_STRING,
    DateField: Date,
    DecimalField: CURRENCY,
}
