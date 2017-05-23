__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""
import logging

from functools import partial
from datetime import datetime, date
from decimal import Decimal, InvalidOperation

from a_tuin.metadata.exceptions import RequiredValueMissing


LOG = logging.getLogger(__name__)


# wrap built in functions in order that a partial can be created for each of them
def _getattr(field, instance):
    return getattr(instance, field)


def _setattr(field, instance, value):
    setattr(instance, field, value)


class Field(object):

    def __init__(self, name, datatype, is_mutable=True, required=False, default=None, description=None, validation=None, use_custom_properties=False):
        self._name = name
        self._type = datatype
        self._is_mutable = is_mutable
        self._is_required = required
        self._default = default
        self._description = description
        self._validation = validation
        self._use_custom_properties = use_custom_properties

        # TODO validate default

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    def derive(self, transformation):
        return transformation(self)

    def type_cast(self, value):
        if value is None or type(value) == self._type:
            return value
        else:
            try:
                return self._type(value)
            except TypeError as err:
                LOG.warning(err)
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
            raise RequiredValueMissing(self)
        return value

    def create_property_on_class(self, cls, internal_name):
        """ Automatically create a property for this field on a class

        TODO - Is this the simplest thing that could work?
            What about not hiding some members?

        :param cls: class to add the property to
        :param internal_name: name of the protected member to expose
        """
        if not self._use_custom_properties:
            if self._is_mutable:
                setter = partial(_setattr, internal_name)
            else:
                setter = None
            setattr(
                cls,
                self._name,
                property(
                    partial(_getattr, internal_name),
                    setter,
                    None,
                    self._description
                )
            )


class UnusedField(Field):

    def __init__(self, name, is_mutable=True, required=False, default=None, description=None, validation=None, use_custom_properties=False):
        super().__init__(name, str, is_mutable=is_mutable, required=required, default=default, description=description, validation=validation, use_custom_properties=use_custom_properties)


class ObjectReferenceField(Field):

    def __init__(self, name, is_mutable=True, required=False, default=None, description=None, validation=None, use_custom_properties=False):
        super().__init__(name, str, is_mutable=is_mutable, required=required, default=default, description=description, validation=validation, use_custom_properties=use_custom_properties)

    def type_cast(self, value):
        return value


class DenormalisedField(Field):

    def __init__(self, name, extraction, description=None):
        super().__init__(name, str, is_mutable=False, description=description)
        self._extraction = extraction

    def type_cast(self, value):
        return self._extraction(value)


class StringField(Field):

    def __init__(self, name, is_mutable=True, required=False, default=None, description=None, validation=None, use_custom_properties=False, strfmt=None):
        super().__init__(name, str, is_mutable=is_mutable, required=required, default=default, description=description, validation=validation, use_custom_properties=use_custom_properties)
        self._strfmt = strfmt

    def type_cast(self, value):
        if type(value) in (date, datetime) and self._strfmt is not None:
            return value.strftime(self._strfmt)
        return super().type_cast(value)


class BooleanField(Field):
    def __init__(self, name, is_mutable=True, required=False, default=None, description=None, validation=None, use_custom_properties=False):
        super().__init__(name, bool, is_mutable, required, default, description, validation)


class IntField(Field):
    def __init__(self, name, is_mutable=True, required=False, default=None, description=None, validation=None, use_custom_properties=False):
        super().__init__(name, int, is_mutable=is_mutable, required=required, default=default, description=description, validation=validation, use_custom_properties=use_custom_properties)

    def type_cast(self, value):
        if type(value) == datetime:
            return datetime.toordinal(value)
        elif type(value) == date:
            return date.toordinal(value)
        else:
            return super().type_cast(value)


class IntEnumField(IntField):
    def __init__(self, name, enum_class, is_mutable=True, required=False, default=None, description=None, validation=None, use_custom_properties=False):
        super().__init__(name, is_mutable, required, default, description, validation)
        self._enum_class = enum_class

    @property
    def enum_class(self):
        return self._enum_class

    def type_cast(self, value):
        if value is not None:
            return self._enum_class(value)
        else:
            return None


class FloatField(Field):
    def __init__(self, name, is_mutable=True, required=False, default=None, description=None, validation=None, use_custom_properties=False):
        super().__init__(name, float, is_mutable=is_mutable, required=required, default=default, description=description, validation=validation, use_custom_properties=use_custom_properties)

    def type_cast(self, value):
        if type(value) == datetime:
            return datetime.timestamp(value)
        elif type(value) == date:
            return datetime.timestamp(datetime(value.year, value.month, value.day))
        else:
            return super().type_cast(value)


class DecimalField(Field):
    def __init__(self, name, is_mutable=True, required=False, default=None, description=None, validation=None, use_custom_properties=False):
        super().__init__(name, Decimal, is_mutable=is_mutable, required=required, default=default, description=description, validation=validation, use_custom_properties=use_custom_properties)

    def type_cast(self, value):
        if type(value) == self._type:
            return value
        elif not value:
            return None
        else:
            try:
                return self._type(value)
            except InvalidOperation as invop:
                LOG.exception('Invalid operation converting {}'.format(value), invop)
                raise

class DateTimeField(Field):
    def __init__(self, name, is_mutable=True, required=False, default=None, description=None, validation=None, use_custom_properties=False, strfmt='%Y-%m-%d %H:%M:%S'):
        super().__init__(name, datetime, is_mutable=is_mutable, required=required, default=default, description=description, validation=validation, use_custom_properties=use_custom_properties)
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
    def __init__(self, name, is_mutable=True, required=False, default=None, description=None, validation=None, use_custom_properties=False, strfmt='%Y-%m-%d'):
        super().__init__(name, date, is_mutable=is_mutable, required=required, default=default, description=description, validation=validation, use_custom_properties=use_custom_properties)
        self._strfmt = strfmt

    def type_cast(self, value):
        value_type = type(value)
        if value_type == self._type:
            return value
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
    (ObjectReferenceField, IntEnumField),
    (ObjectReferenceField, FloatField),
    (ObjectReferenceField, DecimalField),
    (ObjectReferenceField, DateTimeField),
    (ObjectReferenceField, DateField),
    # TODO expand on the options here
)
