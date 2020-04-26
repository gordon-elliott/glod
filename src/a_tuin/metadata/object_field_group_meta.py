__copyright__ = 'Copyright(c) Gordon Elliott 2017'

from a_tuin.metadata import ObjectFieldGroup, ArgsFieldGroup, prefix_name_with_underscore, Mapping


class ObjectFieldGroupMeta(type):
    def __init__(cls, what, bases=None, dict_=None):
        super().__init__(what, bases, dict_)

        if hasattr(cls, 'public_interface'):
            # create a class with a specific set of fields
            class SpecificObjectFieldGroup(ObjectFieldGroup):
                def __init__(self, fields):
                    super().__init__(fields, cls)

            # field group for the constructor parameters
            cls.constructor_parameters = ArgsFieldGroup(cls.public_interface)
            # field group for the public properties
            cls.properties = SpecificObjectFieldGroup(cls.public_interface)
            # field group for private members
            cls.internal = cls.constructor_parameters.derive(prefix_name_with_underscore, SpecificObjectFieldGroup)
            # mapping from constructor params to private members
            cls.constructor_to_internal = Mapping(cls.constructor_parameters, cls.internal)
            # mapping from public properties to private members
            cls.properties_to_internal = Mapping(cls.properties, cls.internal)

            # dynamically create properties
            for property_field, internal in cls.properties_to_internal:
                property_field.create_property_on_class(cls, internal.name)

    def __call__(self, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        self.constructor_to_internal.update_in_place((args, kwargs), instance)
        return instance


class ObjectFieldGroupBase(object, metaclass=ObjectFieldGroupMeta):

    # meta class __call__ takes care of assigning members from parameters
    def __init__(self, *args, **kwargs):
        pass

    def update_from(self, input_dict):
        self.properties.update_instance_from_dict(self, input_dict)
