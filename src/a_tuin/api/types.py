__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene
from graphene.types.datetime import DateTime

from a_tuin.metadata import (
    BooleanField,
    IntField,
    StringField,
    DateField,
    DecimalField,
    IntEnumField,
)


GRAPHENE_FIELD_TYPE_MAP = {
    BooleanField: graphene.Boolean,
    IntField: graphene.Int,
    StringField: graphene.String,
    DateField: DateTime,
    DecimalField: graphene.Float,
    IntEnumField: graphene.Enum,
    # TODO map date and Decimal to custom types
}

OBJECT_REFERENCE_MAP = {
}
