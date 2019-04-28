__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""
from sqlalchemy import (
    String,
    Integer,
    Date,
    DateTime,
    Numeric,
    Boolean
)

from a_tuin.metadata import (
    ObjectReferenceField,
    BooleanField,
    IntField,
    StringField,
    DescriptionField,
    DateField,
    DateTimeField,
    DecimalField,
)

REGULAR_STRING = String(64)
DESCRIPTION = String(1024)
CURRENCY = Numeric(scale=2)

DB_COLUMN_TYPE_MAP = {
    ObjectReferenceField: Integer,
    BooleanField: Boolean,
    IntField: Integer,
    StringField: REGULAR_STRING,
    DescriptionField: DESCRIPTION,
    DateField: Date,
    DateTimeField: DateTime,
    DecimalField: CURRENCY,
}
