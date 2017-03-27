__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""
from sqlalchemy import (
    String,
    Integer,
    Date,
    Numeric,
    ForeignKeyConstraint,
    Column,
    Table,
    PrimaryKeyConstraint
)
from sqlalchemy.orm import mapper

from glod.db.metadata import metadata
from glod.metadata import (
    ObjectReferenceField,
    IntField,
    StringField,
    DateField,
    DecimalField,
    prefix_name_with_underscore,
)

ID_COLUMN_NAME = 'id'
ID_FIELDNAME = '_id'

REGULAR_STRING = String(64)
CURRENCY = Numeric(scale=2)

DB_COLUMN_TYPE_MAP = {
    ObjectReferenceField: Integer,
    IntField: Integer,
    StringField: REGULAR_STRING,
    DateField: Date,
    DecimalField: CURRENCY,
}

# TODO backref, eager, lazy loading
# TODO functions to class
# TODO drive from metadata relationships


def db_columns_from_model(model_class):
    columns = {
        ID_FIELDNAME: Column(ID_COLUMN_NAME, Integer, key=ID_FIELDNAME)
    }

    for source, dest in model_class.constructor_to_internal:
        columns[dest.name] = Column(source.name, DB_COLUMN_TYPE_MAP[type(dest)], key=dest.name)

    return columns


def db_constraints_from_model(model_class, fk_constraints=None, primary_key_fieldname=ID_FIELDNAME):
    constraints = {
        ID_FIELDNAME: PrimaryKeyConstraint(ID_FIELDNAME),
    }
    if fk_constraints:
        for sources, destinations in fk_constraints:
            constraints[sources] = ForeignKeyConstraint(sources, destinations)
    return constraints


def do_map(model_class, table_name, columns, constraints):

    table = Table(table_name, metadata, *columns.values(), *constraints.values())
    mapper(model_class, table)


def db_fk_from_model(columns, fk_fieldname, fk_column_name, object_ref_fieldname, referenced_pk_fieldname):
    del columns[object_ref_fieldname]
    columns[fk_fieldname] = Column(fk_column_name, Integer, key=fk_fieldname)
    fk_constraint = ((fk_fieldname,), (referenced_pk_fieldname,))
    return fk_constraint