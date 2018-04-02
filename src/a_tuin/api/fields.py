__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

import graphene
import logging

from collections import OrderedDict
from functools import partial, lru_cache

from a_tuin.metadata import ObjectReferenceField
from a_tuin.api.types import GRAPHENE_FIELD_TYPE_MAP, OBJECT_REFERENCE_MAP, GRAPHENE_TYPE_MAP


RESERVED_FIELD_NAMES = ('type',)
LOG = logging.getLogger(__name__)


class FieldNameReserved(Exception):
    pass


def _check_field_name_is_not_reserved(field):
    if field.name.lower() in RESERVED_FIELD_NAMES:
        raise FieldNameReserved("Unable to map field. '{}' is a reserved name.".format(field.name))


@lru_cache()
def _get_enum_type(field):
    """ Create a graphene Enum from the Python enum
        Make sure that the enum type is reused by memoizing the function

    :param field a_tuin.metadata.Field:
    :return:
    """
    return graphene.Enum.from_enum(field.enum_class)


def _map_mounted_field(model_class):
    """ Produce a Graphene field for a model metadata Field

    :param model_class: class to inspect
    :yield: tuple of field name an mounted graphene field
    """
    for field in model_class.public_interface:
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


def _map_argument(model_class):
    """ Produce a Graphene argument for a model metadata Field

    :param model_class: class to inspect
    :yield: tuple of field name an mounted graphene argument
    """
    for field in model_class.public_interface:
        _check_field_name_is_not_reserved(field)
        graphene_field_type = GRAPHENE_FIELD_TYPE_MAP.get(type(field))
        argument_name = field.name
        if graphene_field_type is None and hasattr(field, 'enum_class'):
            graphene_field_type = _get_enum_type(field)

        if graphene_field_type is None and isinstance(field, ObjectReferenceField):
            graphene_field_type = GRAPHENE_TYPE_MAP.get(field.type)

        if graphene_field_type:
            yield argument_name, graphene.Argument(graphene_field_type)
        else:
            LOG.warning('Unable to map {}'.format(field))


def _get_mapped_fields(field_mapper, model_class):
    """ Use model metadata to produce Graphene Fields

    :param model_class: class to inspect
    :return: OrderedDict of fieldname to Graphene Field
    """
    return OrderedDict(field_mapper(model_class))


get_local_fields = partial(_get_mapped_fields, _map_mounted_field)
get_input_fields = partial(_get_mapped_fields, _map_argument)
