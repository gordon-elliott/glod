__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""
import logging

from collections import OrderedDict
from operator import getitem, setitem

from a_tuin.metadata.exceptions import FieldAssignmentError, field_errors_check, DATA_LOAD_ERRORS
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

    def fill_instance_from_dict(self, input_dict):
        raise NotImplementedError

    def update_instance_from_dict(self, instance, input_dict):
        raise NotImplementedError

    def iterate_instance(self, instance, per_field_map):
        with field_errors_check() as errors:
            for field in self._fields:
                try:
                    yield field, self._get_value(instance, field), per_field_map.get(field)
                except FieldAssignmentError as field_error:
                    errors.append(field_error)
                except Exception as ex:
                    errors.append(FieldAssignmentError(field, ex))

    def _get_field_index(self, field):
        for i, item in enumerate(self._fields):
            if item == field:
                return i, item
        return None, None

    def _type_cast(self, input_dict):
        cast_values = []
        with field_errors_check() as errors:
            for field in self._fields:
                try:
                    if field.name in input_dict:
                        raw_value = input_dict[field.name]
                    else:
                        raw_value = field.get_value(self, input_dict)
                    cast_values.append((field.name, field.type_cast(raw_value)))
                except FieldAssignmentError as fae:
                    errors.append(fae)
                except DATA_LOAD_ERRORS as ex:
                    errors.append(FieldAssignmentError(field, ex))

        return OrderedDict(cast_values)

    def _group_get_value(self, instance, field):
        raise NotImplementedError

    def _get_value(self, instance, field):
        if field.is_computed:
            return field.get_value(self, instance)
        else:
            return self._group_get_value(instance, field)

    def _accessor(self, instance, key):
        raise NotImplementedError

    #
    # Used in unittests
    #

    def as_dict(self, instance):
        return {
            field.name: self._get_value(instance, field)
            for field in self._fields
        }

    def instances_differ(self, instance, other):
        return any(
            self._get_value(instance, field) != self._get_value(other, field)
            for field in self._fields
        )


class SequenceFieldGroup(FieldGroup):

    def fill_instance_from_dict(self, input_dict):
        values_in_order = self._type_cast(input_dict)
        return self._container_type(values_in_order.values())

    def _accessor(self, instance, key):
        return getitem(instance, key)

    def _group_get_value(self, instance, field):
        index, _ = self._get_field_index(field)
        return self._accessor(instance, index)


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
            if not field.is_computed:
                value = field.prepare_value(value)
                index, _ = self._get_field_index(field)
                return self._mutator(instance, index, value)
        except FieldAssignmentError:
            raise
        except Exception as ex:
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

    def _group_get_value(self, instance, field):
        return self._accessor(instance, field.name)

    def _accessor(self, instance, key):
        return getitem(instance, key)

    def set_value(self, instance, field, value):
        try:
            if not field.is_computed:
                value = field.prepare_value(value)
                return self._mutator(instance, field.name, value)
        except FieldAssignmentError:
            raise
        except Exception as ex:
            raise FieldAssignmentError(field, ex)

    def _mutator(self, instance, key, value):
        return setitem(instance, key, value)


class ObjectFieldGroup(MutableSequenceFieldGroup):

    def fill_instance_from_dict(self, input_dict):
        return self._container_type(**self._type_cast(input_dict))

    def _group_get_value(self, instance, field):
        return self._accessor(instance, field.name)

    def _accessor(self, instance, key):
        return getattr(instance, key)

    def set_value(self, instance, field, value):
        try:
            if not field.is_computed:
                value = field.prepare_value(value)
                return self._mutator(instance, field.name, value)
        except FieldAssignmentError:
            raise
        except Exception as ex:
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
                    yield field, value, per_field_map.get(field)
                except FieldAssignmentError as fae:
                    errors[field] = fae

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

            for field in self._fields:
                try:
                    computed_value = field.get_value(self, input_dict)
                    key_values.append((field.name, computed_value))
                except KeyError:
                    pass

        return OrderedDict(key_values)

    def as_dict(self, instance):
        return OrderedDict(
            (field.name, self._get_value(instance, field))
            for field in self._fields
            if field.name in instance
        )

    def instances_differ(self, instance, other):
        return any(
            self._get_value(instance, field) != self._get_value(other, field)
            for field in self._fields
            if field.name in instance and field.name in other
        )
