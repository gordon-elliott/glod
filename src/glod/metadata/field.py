__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from copy import deepcopy
from datetime import datetime, date
from decimal import Decimal


class Field(object):

    def __init__(self, name, datatype, description=None, validation=None):
        self._name = name
        self._type = datatype
        self._description = description
        self._validation = validation

    def derive(self, transformation):
        target = deepcopy(self)
        transformation(self, target)
        return target

    def type_cast(self, value):
        if type(value) == self._type:
            return value
        else:
            try:
                return self._type(value)
            except TypeError as err:
                print(err)
                raise


class UnusedField(Field):

    def __init__(self, name, description=None, validation=None):
        super().__init__(name, str, description, validation)


class ObjectReferenceField(Field):

    def __init__(self, name, description=None, validation=None):
        super().__init__(name, str, description, validation)

    def type_cast(self, value):
        return value


class StringField(Field):

    def __init__(self, name, description=None, validation=None):
        super().__init__(name, str, description, validation)


class IntField(Field):
    def __init__(self, name, description=None, validation=None):
        super().__init__(name, int, description, validation)

    def type_cast(self, value):
        if type(value) == datetime:
            return datetime.toordinal(value)
        elif type(value) == date:
            return date.toordinal(value)
        else:
            return super().type_cast(value)


class FloatField(Field):
    def __init__(self, name, description=None, validation=None):
        super().__init__(name, float, description, validation)

    def type_cast(self, value):
        if type(value) == datetime:
            return datetime.timestamp(value)
        elif type(value) == date:
            return float(date.toordinal(value))
        else:
            return super().type_cast(value)


class DecimalField(Field):
    def __init__(self, name, description=None, validation=None):
        super().__init__(name, Decimal, description, validation)


class DateTimeField(Field):
    def __init__(self, name, description=None, validation=None, strfmt='%Y-%m-%d %H:%M:%S'):
        super().__init__(name, datetime, description, validation)
        self._strfmt = strfmt

    def type_cast(self, value):
        value_type = type(value)
        if value_type == self._type:
            return value
        elif value_type == str:
            return datetime.strptime(value, self._strfmt)
        elif value_type == float:
            return datetime.fromtimestamp(value)
        elif value_type == int:
            return datetime.fromordinal(value)
        elif value_type == date:
            return datetime.fromordinal(value.toordinal())


class DateField(Field):
    def __init__(self, name, description=None, validation=None, strfmt='%Y-%m-%d'):
        super().__init__(name, date, description, validation)
        self._strfmt = strfmt

    def type_cast(self, value):
        value_type = type(value)
        if value_type == self._type:
            return value
        elif value_type == str:
            return date.fromtimestamp(datetime.strptime(value, self._strfmt).timestamp())
        elif value_type == float:
            return date.fromtimestamp(value)
        elif value_type == int:
            return date.fromordinal(value)
        elif value_type == datetime:
            return date.fromtimestamp(value.timestamp())


INVALID_FIELD_COMBINATIONS = (
    (DecimalField, DateTimeField),
    (DateTimeField, DecimalField),
    (DecimalField, DateField),
    (DateField, DecimalField),
    (ObjectReferenceField, IntField),
    (ObjectReferenceField, FloatField),
    (ObjectReferenceField, DecimalField),
    (ObjectReferenceField, DateTimeField),
    (ObjectReferenceField, DateField),
    # TODO expand on the options here
)