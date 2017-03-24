__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from datetime import datetime, date
from decimal import Decimal, InvalidOperation


class RequiredValueMissing(Exception):
    pass


class Field(object):

    def __init__(self, name, datatype, required=False, default=None, description=None, validation=None):
        self._name = name
        self._type = datatype
        self._is_required = required
        self._default = default
        self._description = description
        self._validation = validation

        # TODO validate default

    @property
    def name(self):
        return self._name

    def derive(self, transformation):
        return transformation(self)

    def type_cast(self, value):
        if value is None or type(value) == self._type:
            return value
        else:
            try:
                return self._type(value)
            except TypeError as err:
                print(err)
                raise

    def is_filled(self, value):
        return not self._is_required or value is not None

    def use_default(self, value):
        return self._default if (
                value is None and
                self._default is not None and
                self._is_required
        ) else value

    def prepare_value(self, value):
        value = self.type_cast(value)
        value = self.use_default(value)
        if not self.is_filled(value):
            raise RequiredValueMissing()
        return value


class UnusedField(Field):

    def __init__(self, name, required=False, default=None, description=None, validation=None):
        super().__init__(name, str, required=required, default=default, description=description, validation=validation)


class ObjectReferenceField(Field):

    def __init__(self, name, required=False, default=None, description=None, validation=None):
        super().__init__(name, str, required=required, default=default, description=description, validation=validation)

    def type_cast(self, value):
        return value


class DenormalisedField(Field):

    def __init__(self, name, extraction, description=None):
        super().__init__(name, str, description=description)
        self._extraction = extraction

    def type_cast(self, value):
        return self._extraction(value)


class StringField(Field):

    def __init__(self, name, required=False, default=None, description=None, validation=None, strfmt=None):
        super().__init__(name, str, required=required, default=default, description=description, validation=validation)
        self._strfmt = strfmt

    def type_cast(self, value):
        if type(value) in (date, datetime) and self._strfmt is not None:
            return value.strftime(self._strfmt)
        return super().type_cast(value)


class IntField(Field):
    def __init__(self, name, required=False, default=None, description=None, validation=None):
        super().__init__(name, int, required=required, default=default, description=description, validation=validation)

    def type_cast(self, value):
        if type(value) == datetime:
            return datetime.toordinal(value)
        elif type(value) == date:
            return date.toordinal(value)
        else:
            return super().type_cast(value)


class FloatField(Field):
    def __init__(self, name, required=False, default=None, description=None, validation=None):
        super().__init__(name, float, required=required, default=default, description=description, validation=validation)

    def type_cast(self, value):
        if type(value) == datetime:
            return datetime.timestamp(value)
        elif type(value) == date:
            return datetime.timestamp(datetime(value.year, value.month, value.day))
        else:
            return super().type_cast(value)


class DecimalField(Field):
    def __init__(self, name, required=False, default=None, description=None, validation=None):
        super().__init__(name, Decimal, required=required, default=default, description=description, validation=validation)

    def type_cast(self, value):
        if type(value) == self._type:
            return value
        elif not value:
            return None
        else:
            try:
                return self._type(value)
            except InvalidOperation as invop:
                print(invop)
                raise

class DateTimeField(Field):
    def __init__(self, name, required=False, default=None, description=None, validation=None, strfmt='%Y-%m-%d %H:%M:%S'):
        super().__init__(name, datetime, required=required, default=default, description=description, validation=validation)
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
    def __init__(self, name, required=False, default=None, description=None, validation=None, strfmt='%Y-%m-%d'):
        super().__init__(name, date, required=required, default=default, description=description, validation=validation)
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