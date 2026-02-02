__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""
from collections import OrderedDict

from a_tuin.metadata.exceptions import FieldAssignmentError, field_errors_check, DATA_LOAD_ERRORS
from a_tuin.metadata.field import INVALID_FIELD_COMBINATIONS


class IncompatibleFieldTypes(Exception):
    pass


class Mapping(object):

    def __init__(self, source_entity, destination_entity, field_mappings=None, field_casts=None):
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
        self._field_casts = field_casts

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

    def _iterate_instance(self, source):
        source_field_to_destination_field = dict(self._field_mappings)
        with field_errors_check() as errors:
            for source_field, value, destination_field in self._source_entity.iterate_instance(
                source, source_field_to_destination_field
            ):
                try:
                    if destination_field is not None:
                        if self._field_casts and source_field.name in self._field_casts:
                            value = self._field_casts[source_field.name](value, destination_field)
                        yield source_field, value, destination_field
                except FieldAssignmentError as field_error:
                    errors.append(field_error)
                except DATA_LOAD_ERRORS as ex:
                    errors.append(FieldAssignmentError(source_field, ex))

    def update_in_place(self, source, destination):
        with field_errors_check() as errors:
            for source_field, value, destination_field in self._iterate_instance(source):
                try:
                    self._destination_entity.set_value(destination, destination_field, value)
                except FieldAssignmentError as field_error:
                    errors.append(field_error)

    def cast_from(self, source):
        input_dict = OrderedDict(
            (destination_field.name, value)
            for source_field, value, destination_field in self._iterate_instance(source)
        )
        return self._destination_entity.fill_instance_from_dict(input_dict)
