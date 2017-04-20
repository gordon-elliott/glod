__copyright__ = 'Copyright(c) Gordon Elliott 2017'

from a_tuin.metadata import ObjectFieldGroup, prefix_name_with_underscore, Mapping


class ObjectFieldGroupMeta(type):
    def __init__(cls, what, bases=None, dict_=None):
        super().__init__(what, bases, dict_)

        if hasattr(cls, 'constructor_parameters'):
            # create a class with a specific set of fields
            class SpecificObjectFieldGroup(ObjectFieldGroup):
                def __init__(self, fields):
                    super().__init__(fields, cls)

            cls.internal = cls.constructor_parameters.derive(prefix_name_with_underscore, SpecificObjectFieldGroup)
# TODO          cls.properties = cls.constructor_parameters.derive(field_group_class=SpecificObjectFieldGroup)
            cls.constructor_to_internal = Mapping(cls.constructor_parameters, cls.internal)

    def __call__(self, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        self.constructor_to_internal.update_in_place((args, kwargs), instance)
        return instance

