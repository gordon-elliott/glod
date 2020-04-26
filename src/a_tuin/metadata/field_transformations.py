__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""
from copy import deepcopy
from graphene.utils.str_converters import to_camel_case


def copy_field(source):
    return deepcopy(source)


def prefix_name_with_underscore(source):
    target = copy_field(source)
    target.name = '_' + source.name
    return target


def replace_underscore_with_space(source):
    target = copy_field(source)
    target.name = source.name.replace('_', ' ')
    return target


def make_boolean(source):
    target = copy_field(source)
    target.type = bool
    return target


def snake_to_camel_case(source):
    target = copy_field(source)
    target.name = to_camel_case(source.name)
    return target
