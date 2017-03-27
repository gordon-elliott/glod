__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

class Reference(object):

    def __init__(self, source_class, source_field_public_name, target_class):
        self._source_class = source_class
        self._source_field_public_name = source_field_public_name
        self._source_field_internal = source_class.constructor_to_internal.get_mapped_by_name(source_field_public_name)
        self._target_class = target_class
