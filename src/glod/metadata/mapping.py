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

    def reverse(self):
        reverse_mappings = tuple(
            (dest, src) for src, dest in self._field_mappings
        )
        return Mapping(
            self._destination_entity,
            self._source_entity,
            reverse_mappings
        )

    def update_in_place(self, source, destination):
        for source_field, destination_field in self._field_mappings:
            value = self._source_entity.get_value(source, source_field)
            self._destination_entity.set_value(destination, destination_field, value)

    def cast_from(self, source):
        input_dict = {
            destination_field._name: self._source_entity.get_value(source, source_field)
            for source_field, destination_field in self._field_mappings
        }
        return self._destination_entity.fill_instance_from_dict(input_dict)