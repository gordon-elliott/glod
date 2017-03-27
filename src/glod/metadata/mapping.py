__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from glod.metadata.field import INVALID_FIELD_COMBINATIONS


class IncompatibleFieldTypes(Exception):
    pass


class Mapping(object):

    def __init__(self, source_entity, destination_entity, field_mappings=None):
        self._source_entity = source_entity
        self._destination_entity = destination_entity

        if not field_mappings:
            field_mappings = tuple(zip(self._source_entity, self._destination_entity))

        mapping_types = set(
            (type(src), type(dest)) for src, dest in field_mappings
        )
        if mapping_types.intersection(set(INVALID_FIELD_COMBINATIONS)):
            raise IncompatibleFieldTypes()

        self._field_mappings = field_mappings

    def __iter__(self):
        self._current_field_index = 0
        return self

    def __next__(self):
        if self._current_field_index >= len(self._field_mappings):
            raise StopIteration

        result = self._field_mappings[self._current_field_index]
        self._current_field_index += 1

        return result

    def __len__(self):
        return len(self._field_mappings)

    def reverse(self):
        reverse_mappings = tuple(
            (dest, src) for src, dest in self._field_mappings
        )
        return Mapping(
            self._destination_entity,
            self._source_entity,
            reverse_mappings
        )

    def get_mapped_by_name(self, source_name):
        for src, dest in self._field_mappings:
            if src.name == source_name:
                return dest
        return None

    def update_in_place(self, source, destination):
        for source_field, destination_field in self._field_mappings:
            value = self._source_entity.get_value(source, source_field)
            self._destination_entity.set_value(destination, destination_field, value)

    def cast_from(self, source):
        input_dict = {
            destination_field.name: self._source_entity.get_value(source, source_field)
            for source_field, destination_field in self._field_mappings
        }
        return self._destination_entity.fill_instance_from_dict(input_dict)