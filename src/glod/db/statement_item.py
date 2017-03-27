__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""
from sqlalchemy.orm import relationship

from glod.db.mapper import do_map, db_columns_from_model, db_constraints_from_model, db_fk_from_model
from glod.model.statement_item import StatementItem
from glod.model.references import statement_item__account


class Relation(object):
    def __init__(self, reference, referenced_pk_fieldname, **kwargs):
        self._reference = reference
        self._referenced_pk_fieldname = referenced_pk_fieldname
        self._relationship_args = kwargs

    @property
    def fk_fieldname(self):
        return '{}_id'.format(self._reference._source_field_internal.name)

    @property
    def object_ref_fieldname(self):
        return self._reference._source_field_internal.name

    @property
    def fk_column_name(self):
        return '{}_id'.format(self._reference._source_field_public_name)

    def mapper_properties(self):
        target = self._reference._target_class
        return (
            self.object_ref_fieldname,
            relationship(target, **self._relationship_args)
        )

    def mapper_constraint(self, columns):
        fk_constraint = db_fk_from_model(
            columns,
            self.fk_fieldname,
            self.fk_column_name,
            self.object_ref_fieldname,
            self._referenced_pk_fieldname
        )
        return fk_constraint

relation = Relation(
    statement_item__account,
    'account._id',
    backref='statement_items',
    lazy='joined'
)

columns = db_columns_from_model(StatementItem)
fk_constraints = (relation.mapper_constraint(columns),)
constraints = db_constraints_from_model(StatementItem, fk_constraints)
do_map(StatementItem, 'statement_item', columns, constraints)

