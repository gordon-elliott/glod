__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""
import logging

from collections import OrderedDict
from operator import getitem, setitem

from a_tuin.metadata.exceptions import FieldAssignmentError, FieldErrors, field_errors_check
from a_tuin.metadata.field_transformations import copy_field


LOG = logging.getLogger(__name__)


class FieldGroup(object):

    def __init__(self, fields, container_type):
        self._fields = fields
        self._container_type = container_type

    def __iter__(self):
        self._current_field_index = 0
        return self

    def __next__(self):
        if self._current_field_index >= len(self._fields):
            raise StopIteration

        result = self._fields[self._current_field_index]
        self._current_field_index += 1

        return result

    def __len__(self):
        return len(self._fields)

    def __getitem__(self, key):
        for field in self._fields:
            if field.name == key:
                return field
        raise KeyError('{} not found.'.format(key))

    def __setitem__(self, key, replacement_field):

        assert key == replacement_field.name, 'Key does not match field name.'

        # replace field
        for i, field in enumerate(self._fields):
            if field.name == key:
                self._fields[i] = replacement_field
                break

    def derive(self, transformation=None, field_group_class=None):
        transformation = copy_field if transformation is None else transformation
        field_group_class = field_group_class if field_group_class else self.__class__
        return field_group_class(
            [
                field.derive(transformation)
                for field in self._fields
            ]
        )

    def _iterate_fields(self, catch=FieldAssignmentError, throw=FieldErrors):
        """ Iterate through the fields catching specified exceptions, collecting
            them and then throwing a single exception when all fields have been
            processed

        :param catch: Exception(s) to catch
        :param throw: Exception to throw at the end
        """
        with field_errors_check(throw) as errors:
            for field in self._fields:
                try:
                    yield field
                except catch as field_error:
                    errors.append(field_error)

    def _get_values_in_order(self, input_dict):
        return [
            field.type_cast(input_dict[field.name])
            for field in self._iterate_fields()
        ]

    def fill_instance_from_dict(self, input_dict):
        raise NotImplementedError

    def update_instance_from_dict(self, instance, input_dict):
        raise NotImplementedError

    def iterate_instance(self, instance, per_field_map):
        for field in self._iterate_fields():
            yield field, self.get_value(instance, field), per_field_map.get(field)

    def _get_field_index(self, field):
        for i, item in enumerate(self._fields):
            if item == field:
                return i, item
        return None, None

    def _type_cast(self, input_dict):
        return {
            field.name: field.type_cast(input_dict[field.name])
            for field in self._iterate_fields()
        }

    def get_value(self, instance, field):
        raise NotImplementedError

    def as_dict(self, instance):
        return {
            field.name: self.get_value(instance, field)
            for field in self._iterate_fields()
        }

    def _accessor(self, instance, key):
        raise NotImplementedError

    def instances_differ(self, instance, other):
        return any(
            self.get_value(instance, field) != self.get_value(other, field)
            for field in self._iterate_fields()
        )


class SequenceFieldGroup(FieldGroup):

    def fill_instance_from_dict(self, input_dict):
        values_in_order = self._get_values_in_order(input_dict)
        return self._container_type(values_in_order)

    def _accessor(self, instance, key):
        return getitem(instance, key)

    def get_value(self, instance, field):
        index, _ = self._get_field_index(field)
        value = self._accessor(instance, index)
        return field.conform_value(value)


class TupleFieldGroup(SequenceFieldGroup):

    def __init__(self, fields):
        super().__init__(fields, tuple)


class MutableSequenceFieldGroup(FieldGroup):

    def update_instance_from_dict(self, instance, input_dict):
        with field_errors_check() as errors:
            for field_name, value in input_dict.items():
                field = self[field_name]
                try:
                    self.set_value(instance, field, value)
                except FieldAssignmentError as fae:
                    if isinstance(fae.original_exception, AttributeError):
                        LOG.warning('Unable to assign {} to {}'.format(value, field_name))
                    else:
                        errors[field] = fae

    def set_value(self, instance, field, value):
        raise NotImplementedError

    def _mutator(self, instance, key, value):
        raise NotImplementedError

    def empty_instance(self):
        return self._container_type()


class ListFieldGroup(MutableSequenceFieldGroup, SequenceFieldGroup):

    def __init__(self, fields):
        super().__init__(fields, list)

    def set_value(self, instance, field, value):
        try:
            value = field.prepare_value(value)
            index, _ = self._get_field_index(field)
            return self._mutator(instance, index, value)
        except Exception as ex:
            if isinstance(ex, FieldAssignmentError):
                raise
            else:
                raise FieldAssignmentError(field, ex)

    def _mutator(self, instance, key, value):
        return setitem(instance, key, value)

    def empty_instance(self):
        return [None] * len(self)


class DictFieldGroup(MutableSequenceFieldGroup):

    def __init__(self, fields, container_type=None):
        container_type = dict if not container_type else container_type
        super().__init__(fields, container_type)

    def fill_instance_from_dict(self, input_dict):
        return self._container_type(self._type_cast(input_dict))

    def get_value(self, instance, field):
        value = self._accessor(instance, field.name)
        return field.conform_value(value)

    def _accessor(self, instance, key):
        return getitem(instance, key)

    def set_value(self, instance, field, value):
        try:
            value = field.prepare_value(value)
            return self._mutator(instance, field.name, value)
        except Exception as ex:
            if isinstance(ex, FieldAssignmentError):
                raise
            else:
                raise FieldAssignmentError(field, ex)

    def _mutator(self, instance, key, value):
        return setitem(instance, key, value)


class ObjectFieldGroup(MutableSequenceFieldGroup):

    def fill_instance_from_dict(self, input_dict):
        return self._container_type(**self._type_cast(input_dict))

    def get_value(self, instance, field):
        value = self._accessor(instance, field.name)
        return field.conform_value(value)

    def _accessor(self, instance, key):
        return getattr(instance, key)

    def set_value(self, instance, field, value):
        try:
            value = field.prepare_value(value)
            return self._mutator(instance, field.name, value)
        except Exception as ex:
            if isinstance(ex, FieldAssignmentError):
                raise
            else:
                raise FieldAssignmentError(field, ex)

    def _mutator(self, instance, key, value):
        return setattr(instance, key, value)


class PartialDictFieldGroup(DictFieldGroup):

    def __init__(self, fields):
        super().__init__(fields, OrderedDict)

    def iterate_instance(self, instance, per_field_map):
        with field_errors_check() as errors:
            for fieldname, value in instance.items():
                field = self[fieldname]
                try:
                    yield field, field.conform_value(value), per_field_map.get(field)
                except FieldAssignmentError as fae:
                    errors[field] = fae

    def _get_values_in_order(self, input_dict):
        return [
            field.type_cast(input_dict[field.name])
            for field in self._fields
            if field.name in input_dict
        ]

    def _type_cast(self, input_dict):
        field_and_value = (
            (fieldname, self[fieldname], value)
            for fieldname, value in input_dict.items()
        )

        key_values = []

        with field_errors_check() as errors:
            for fieldname, field, value in field_and_value:
                try:
                    key_values.append((fieldname, field.type_cast(value)))
                except FieldAssignmentError as fae:
                    errors[field] = fae

        return OrderedDict(key_values)

    def as_dict(self, instance):
        return OrderedDict(
            (field.name, self.get_value(instance, field))
            for field in self._iterate_fields()
            if field.name in instance
        )

    def instances_differ(self, instance, other):
        return any(
            self.get_value(instance, field) != self.get_value(other, field)
            for field in self._iterate_fields()
            if field.name in instance and field.name in other
        )
