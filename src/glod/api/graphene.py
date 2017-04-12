__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from collections import OrderedDict

import graphene

from glod.api.types import GRAPHENE_FIELD_TYPE_MAP, OBJECT_REFERENCE_MAP


def map_field(field):
    graphene_field_type = GRAPHENE_FIELD_TYPE_MAP.get(type(field))
    if graphene_field_type is None:
        if hasattr(field, 'enum_class'):
            graphene_field_type = graphene.Enum.from_enum(field.enum_class)
        else:
            return graphene.Field(OBJECT_REFERENCE_MAP[field.name])

    return graphene.Field.mounted(graphene_field_type())


def get_local_fields(model_class):
    return OrderedDict(
        (field.name, map_field(field))
        for field in model_class.constructor_parameters
    )
