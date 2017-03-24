__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from datetime import datetime
from decimal import Decimal
from itertools import product

from glod.metadata.field_group import (
    TupleFieldGroup,
    ListFieldGroup,
    DictFieldGroup,
    ObjectFieldGroup,
)
from glod.metadata.field import (
    StringField,
    IntField,
    FloatField,
    DecimalField,
    DateTimeField,
    INVALID_FIELD_COMBINATIONS
)


class _ObjectFieldGroupInstanceFixture(object):
    def __init__(self, name, count, rate, amount, timestamp):
        self.name = name
        self.count = count
        self.rate = rate
        self.amount = amount
        self.timestamp = timestamp


class _ObjectFieldGroupFixture(ObjectFieldGroup):
    def __init__(self, fields):
        super().__init__(fields, _ObjectFieldGroupInstanceFixture)


MUTABLE_FIELD_GROUP_CLASSES = (ListFieldGroup, DictFieldGroup, _ObjectFieldGroupFixture)
FIELD_GROUP_CLASSES = (TupleFieldGroup,) + MUTABLE_FIELD_GROUP_CLASSES
FIELDS = (
    StringField('name', 'Name of this entity'),
    IntField('count'),
    FloatField('rate'),
    DecimalField('amount'),
    DateTimeField('timestamp')
)
DATETIME_FIXTURE = datetime.now()
INITIAL_VALUES = {
    'name': 'initial name',
    'count': 4,
    'rate': 1.243,
    'amount': Decimal('3.22'),
    'timestamp': DATETIME_FIXTURE
}
FIELD_COMBINATIONS = (
    (src, dest)
    for src, dest in product(FIELDS, FIELDS)
    if (type(src), type(dest)) not in INVALID_FIELD_COMBINATIONS
)


def field_group_fixtures(fields=None, field_group_classes=None):
    fields = fields if fields else FIELDS
    field_group_classes = field_group_classes if field_group_classes else FIELD_GROUP_CLASSES

    def dict_as_sequence(d, sequence_type):
        return sequence_type(
            d[field.name] for field in fields
        )

    fixture_constructors = {
        DictFieldGroup: lambda iv: iv.copy(),
        ListFieldGroup: lambda iv: dict_as_sequence(iv, list),
        TupleFieldGroup: lambda iv: dict_as_sequence(iv, tuple),
        _ObjectFieldGroupFixture: lambda iv: _ObjectFieldGroupInstanceFixture(**iv),
    }

    for field_group_class in field_group_classes:
        yield (
            field_group_class,
            field_group_class(fields),
            fixture_constructors[field_group_class]
        )


def field_group_combinations(source_fields=None, destination_fields=None):
    return product(
        field_group_fixtures(source_fields),
        field_group_fixtures(destination_fields)
    )


def inplace_field_group_combinations():
    return product(
        field_group_fixtures(),
        field_group_fixtures(
            field_group_classes=MUTABLE_FIELD_GROUP_CLASSES
        )
    )
