__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

import graphene

from collections import OrderedDict
from functools import partial, lru_cache

from a_tuin.api.types import GRAPHENE_FIELD_TYPE_MAP, OBJECT_REFERENCE_MAP


RESERVED_FIELD_NAMES = ('type',)


class FieldNameReserved(Exception):
    pass


def _check_field_name_is_not_reserved(field):
    if field.name.lower() in RESERVED_FIELD_NAMES:
        raise FieldNameReserved("Unable to map field. '{}' is a reserved name.".format(field.name))


@lru_cache()
def _get_enum_type(field):
    """ Create a graphene Enum from the Python enum
        Make sure that the enum type is reused by memoizing the funtion

    :param field a_tuin.metadata.Field:
    :return:
    """
    return graphene.Enum.from_enum(field.enum_class)


def _map_mounted_field(fields):
    """ Produce a Graphene field for a model metadata Field

    :param fields iterable of a_tuin.metadata.Field:
    :yield: tuple of field name an mounted graphene field
    """
    for field in fields:
        _check_field_name_is_not_reserved(field)
        graphene_field_type = GRAPHENE_FIELD_TYPE_MAP.get(type(field))
        if graphene_field_type is None:
            if hasattr(field, 'enum_class'):
                graphene_field_type = _get_enum_type(field)
                mounted = graphene.Field.mounted(graphene_field_type())
            else:
                mounted = graphene.Field(OBJECT_REFERENCE_MAP[field.name])
        else:
            mounted = graphene.Field.mounted(graphene_field_type())

        yield field.name, mounted


def _map_argument(fields):
    """ Produce a Graphene argument for a model metadata Field

    :param fields iterable of a_tuin.metadata.Field:
    :yield: tuple of field name an mounted graphene argument
    """
    for field in fields:
        _check_field_name_is_not_reserved(field)
        graphene_field_type = GRAPHENE_FIELD_TYPE_MAP.get(type(field))
        if graphene_field_type is None:
            if hasattr(field, 'enum_class'):
                graphene_field_type = _get_enum_type(field)

        if graphene_field_type:
            yield field.name, graphene.Argument(graphene_field_type)


def _get_mapped_fields(field_mapper, model_class):
    """ Use model metadata to produce Graphene Fields

    :param model_class: class to inspect
    :return: OrderedDict of fieldname to Graphene Field
    """
    return OrderedDict(field_mapper(model_class.public_interface))


get_local_fields = partial(_get_mapped_fields, _map_mounted_field)
get_input_fields = partial(_get_mapped_fields, _map_argument)
