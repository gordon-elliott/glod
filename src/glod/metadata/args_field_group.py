__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from glod.metadata.field_group import FieldGroup, TupleFieldGroup, DictFieldGroup


class ArgsFieldGroup(FieldGroup):
    """ Composite field group for parameter lists
    """

    def __init__(self, fields):
        super().__init__(fields, None)
        self._args = TupleFieldGroup(fields)
        self._kwargs = DictFieldGroup(fields)

    def get_value(self, instance, field):
        args, kwargs = instance

        try:
            value = self._args.get_value(args, field)
        except IndexError:
            try:
                value = self._kwargs.get_value(kwargs, field)
            except KeyError:
                value = None

        return value

    def fill_instance_from_dict(self, input_dict):
        return self._kwargs.fill_instance_from_dict(input_dict)


