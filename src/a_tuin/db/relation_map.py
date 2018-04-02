__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship


class RelationMap(object):
    def __init__(self, reference, referenced_pk_fieldname, **kwargs):
        self._reference = reference
        reference.relation_map = self
        self._referenced_pk_fieldname = referenced_pk_fieldname
        self._relationship_args = kwargs

    @property
    def fk_fieldname(self):
        return '{}_id'.format(self._reference.source_field_internal_name)

    @property
    def object_ref_fieldname(self):
        return self._reference.source_field_internal_name

    @property
    def fk_column_name(self):
        return '{}_id'.format(self._reference.source_field_public_name)

    def mapper_properties(self):
        target = self._reference.target_model_class
        return (
            self.object_ref_fieldname,
            relationship(target, **self._relationship_args)
        )

    def mapper_constraint(self, columns):
        del columns[self.object_ref_fieldname]
        columns[self.fk_fieldname] = Column(self.fk_column_name, Integer, key=self.fk_fieldname)
        fk_constraint = ((self.fk_fieldname,), (self._referenced_pk_fieldname,))
        return fk_constraint
