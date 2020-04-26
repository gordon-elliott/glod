__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from graphene import Node, Interface

from a_tuin.api import get_local_fields


def leaf_class_interfaces(model_class):

    model_class_fields = get_local_fields(model_class)
    field_interface_classname = '{}Fields'.format(model_class.__name__)

    return (Node, type(field_interface_classname, (Interface,), model_class_fields))
