__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from sqlalchemy import (
    Column,
    Integer,
    PrimaryKeyConstraint,
    ForeignKeyConstraint,
    Table
)
from sqlalchemy.orm import registry

from a_tuin.db.metadata import metadata
from a_tuin.metadata import IntField


mapper_registry = registry()

ID_COLUMN_NAME = 'id'
ID_FIELDNAME = '_id'
ID_PROPERTY_NAME = 'id'


class TableMap(object):
    def __init__(self, model_class, schema, table_name, db_column_type_map, *relation_maps):
        self._model_class = model_class
        self._schema = schema
        self._table_name = table_name
        self._db_column_type_map = db_column_type_map
        self._relation_maps = relation_maps

        self._db_table_mapper()

    def _db_columns_from_model(self):
        # now that model class is connected to the DB expose a readonly property for the id
        id_field = IntField(ID_PROPERTY_NAME, is_mutable=False)
        id_field.create_property_on_class(self._model_class, ID_FIELDNAME)

        # map the id column
        columns = {
            ID_FIELDNAME: Column(ID_COLUMN_NAME, Integer, key=ID_FIELDNAME)
        }

        for source, dest in self._model_class.constructor_to_internal:
            columns[dest.name] = Column(source.name, self._db_column_type_map[type(dest)], key=dest.name)

        return columns

    def _db_constraints_from_model(self, columns):
        fk_constraints = tuple(
            relation_map.mapper_constraint(self._schema, columns)
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

        self._table = Table(
            self._table_name, metadata, *columns.values(), *constraints.values(), schema=self._schema
        )
        self._model_class.c = self._table.c
        mapper_registry.map_imperatively(self._model_class, self._table, properties=fk_properties)
