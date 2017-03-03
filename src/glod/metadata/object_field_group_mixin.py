__copyright__ = 'Copyright(c) Gordon Elliott 2017'

from glod.metadata import ObjectFieldGroup, prefix_name_with_underscore, Mapping


class ObjectFieldGroupMixin(object):

    def map_constructor_to_internal(self, constructor):
        class SpecificObjectFieldGroup(ObjectFieldGroup):
            def __init__(self, fields):
                super().__init__(fields, self.__class__)

        internal = constructor.derive(prefix_name_with_underscore, SpecificObjectFieldGroup)
        constructor_to_internal = Mapping(constructor, internal)
        return constructor_to_internal