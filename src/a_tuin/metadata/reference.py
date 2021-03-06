__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""


REFERENCES = []


class Reference(object):

    def __init__(self, source_class, source_field_public_name, target_class):
        self._source_class = source_class
        self._source_field_public_name = source_field_public_name
        self._source_field_internal = source_class.constructor_to_internal.get_mapped_by_name(source_field_public_name)
        self._target_class = target_class

    @property
    def source_model_class(self):
        return self._source_class

    @property
    def source_field_internal_name(self):
        return self._source_field_internal.name

    @property
    def source_field_public_name(self):
        return self._source_field_public_name

    @property
    def target_model_class(self):
        return self._target_class


def references_from(model_class):
    return (
        reference
        for reference in REFERENCES
        if reference.source_model_class == model_class
    )


def references_from_field(model_class, source_field_public_name):
    return (
        reference
        for reference in references_from(model_class)
        if reference.source_field_public_name == source_field_public_name
    )
