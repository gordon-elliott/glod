__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from sqlalchemy import Column, Integer, PrimaryKeyConstraint, ForeignKeyConstraint, Table
from sqlalchemy.orm import mapper

from glod.db.mapper import DB_COLUMN_TYPE_MAP
from glod.db.metadata import metadata

ID_COLUMN_NAME = 'id'
ID_FIELDNAME = '_id'


class TableMap(object):
    def __init__(self, model_class, table_name, *relation_maps):
        self._model_class = model_class
        self._table_name = table_name
        self._relation_maps = relation_maps

        self._db_table_mapper()

    def _db_columns_from_model(self):
        columns = {
            ID_FIELDNAME: Column(ID_COLUMN_NAME, Integer, key=ID_FIELDNAME)
        }

        for source, dest in self._model_class.constructor_to_internal:
            columns[dest.name] = Column(source.name, DB_COLUMN_TYPE_MAP[type(dest)], key=dest.name)

        return columns

    def _db_constraints_from_model(self, columns):
        fk_constraints = tuple(
            relation_map.mapper_constraint(columns)
            for relation_map in self._relation_maps
        )
        constraints = {
            ID_FIELDNAME: PrimaryKeyConstraint(ID_FIELDNAME),
        }
        if fk_constraints:
            for sources, destinations in fk_constraints:
                constraints[sources] = ForeignKeyConstraint(sources, destinations)
        return constraints

    def _db_table_mapper(self):
        columns = self._db_columns_from_model()
        fk_properties = dict(
            relation_map.mapper_properties()
            for relation_map in self._relation_maps
        )
        constraints = self._db_constraints_from_model(columns)

        table = Table(self._table_name, metadata, *columns.values(), *constraints.values())
        mapper(self._model_class, table, properties=fk_properties)