__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import graphene

from collections import OrderedDict

from glod.api.types import GRAPHENE_FIELD_TYPE_MAP, OBJECT_REFERENCE_MAP

# TODO consider moving to a_tuin

def _map_field(field):
    """ Produce a Graphene field for a model metadata Field

    :param field a_tuin.metadata.Field:
    :return: graphene.Field
    """
    graphene_field_type = GRAPHENE_FIELD_TYPE_MAP.get(type(field))
    if graphene_field_type is None:
        if hasattr(field, 'enum_class'):
            graphene_field_type = graphene.Enum.from_enum(field.enum_class)
        else:
            return graphene.Field(OBJECT_REFERENCE_MAP[field.name])

    return graphene.Field.mounted(graphene_field_type())


def get_local_fields(model_class):
    """ Use model metadata to produce Graphene Fields

    :param model_class: class to inspect
    :return: OrderedDict of fieldname to Graphene Field
    """
    return OrderedDict(
        (field.name, _map_field(field))
        for field in model_class.constructor_parameters
    )
