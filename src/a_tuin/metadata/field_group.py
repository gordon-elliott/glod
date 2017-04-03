__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from operator import getitem, setitem

from a_tuin.metadata.field_derivations import copy_field


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
        raise KeyError

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

    def _get_values_in_order(self, input_dict):
        return [
            field.type_cast(input_dict[field.name])
            for field in self._fields
        ]

    def fill_instance_from_dict(self, input_dict):
        raise NotImplementedError

    def _get_field_index(self, field):
        for i, item in enumerate(self._fields):
            if item == field:
                return i, item
        return None, None

    def _type_cast(self, input_dict):
        return {
            field.name: field.type_cast(input_dict[field.name])
            for field in self._fields
        }

    def get_value(self, instance, field):
        raise NotImplementedError

    def as_dict(self, instance):
        return {
            field.name: self.get_value(instance, field)
            for field in self._fields
        }

    def _accessor(self, instance, key):
        raise NotImplementedError

    def instances_differ(self, instance, other):
        return any(
            self.get_value(instance, field) != self.get_value(other, field)
            for field in self._fields
        )


class TupleFieldGroup(FieldGroup):

    def __init__(self, fields):
        super().__init__(fields, tuple)

    def fill_instance_from_dict(self, input_dict):
        values_in_order = self._get_values_in_order(input_dict)
        return self._container_type(values_in_order)

    def get_value(self, instance, field):
        index, _ = self._get_field_index(field)
        value = self._accessor(instance, index)
        return field.conform_value(value)

    def _accessor(self, instance, key):
        return getitem(instance, key)


class MutableSequenceFieldGroup(FieldGroup):

    def set_value(self, instance, field, value):
        raise NotImplementedError

    def _mutator(self, instance, key, value):
        raise NotImplementedError

    def empty_instance(self):
        return self._container_type()


class ListFieldGroup(MutableSequenceFieldGroup):

    def __init__(self, fields):
        super().__init__(fields, list)

    def fill_instance_from_dict(self, input_dict):
        values_in_order = self._get_values_in_order(input_dict)
        return self._container_type(values_in_order)

    def get_value(self, instance, field):
        index, _ = self._get_field_index(field)
        value = self._accessor(instance, index)
        return field.conform_value(value)

    def _accessor(self, instance, key):
        return getitem(instance, key)

    def set_value(self, instance, field, value):
        value = field.prepare_value(value)
        index, _ = self._get_field_index(field)
        return self._mutator(instance, index, value)

    def _mutator(self, instance, key, value):
        return setitem(instance, key, value)

    def empty_instance(self):
        return [None] * len(self)


class DictFieldGroup(MutableSequenceFieldGroup):

    def __init__(self, fields):
        super().__init__(fields, dict)

    def fill_instance_from_dict(self, input_dict):
        return self._container_type(self._type_cast(input_dict))

    def get_value(self, instance, field):
        value = self._accessor(instance, field.name)
        return field.conform_value(value)

    def _accessor(self, instance, key):
        return getitem(instance, key)

    def set_value(self, instance, field, value):
        value = field.prepare_value(value)
        return self._mutator(instance, field.name, value)

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
        value = field.prepare_value(value)
        return self._mutator(instance, field.name, value)

    def _mutator(self, instance, key, value):
        return setattr(instance, key, value)
