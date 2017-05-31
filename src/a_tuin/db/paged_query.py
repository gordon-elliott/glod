__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from sqlalchemy import func, asc, desc
from sqlalchemy.orm import joinedload

from a_tuin.db.query import Query


ROW_NUMBER_COLUMN_NAME = '_row_number'


class PagedQuery(Query):
    """ Provide paging logic on a result set by including a row number
        with the entity columns. The row number starts at 1 so it needs
        to be adjusted to a zero-based index.

        Order in which sorting and paging criteria are applied is very
        sensitive so inputs are collected and then applied to a query on
        demand.

    """

    def __init__(self, model_class, model_collection, session):
        super().__init__(model_class, model_collection, session)

        self._filter_criteria = None
        self._sort_criteria = None
        self._offset = None
        self._limit = None
        self._options = None

    def offset(self, offset):
        self._offset = offset
        return self

    def limit(self, num_items):
        self._limit = num_items
        return self

    def joined_load(self, entity):
        self._options = joinedload(entity)
        return self

    def criteria_from_dict(self, filters):
        columns_collection = self._model_class.c
        for filter_field, filter_value in filters.items():
            column = columns_collection.get(filter_field)
            if column is not None:
                yield column.__eq__(filter_value)
                # TODO allow custom operators

    def filter(self, *criteria):
        self._filter_criteria = criteria
        return self

    def sort_criteria_from_dict(self, order_by):
        columns_collection = self._model_class.c
        for fieldname, is_ascending in order_by.items():
            direction = asc if is_ascending else desc
            column = columns_collection.get(fieldname)
            if column is not None:
                yield direction(column)

    def order_by(self, *criteria):
        self._sort_criteria = criteria
        return self

    def _prepare_query(self):
        query = self._session.query(self._model_class)

        if self._options:
            query = query.options(self._options)

        if self._filter_criteria:
            query = query.filter(*self._filter_criteria)

        if self._sort_criteria:
            query = query.order_by(*self._sort_criteria)
            self._row_number_column = func.row_number().over(order_by=self._sort_criteria).label(ROW_NUMBER_COLUMN_NAME)
        else:
            self._row_number_column = func.row_number().over().label(ROW_NUMBER_COLUMN_NAME)
        query = query.add_columns(self._row_number_column)

        if self._offset is not None:
            query = query.from_self().filter(self._row_number_column > self._offset + 1)

        if self._limit is not None:
            query = query.limit(self._limit)

        return query

    def _peel_off_row_number(self, rows):
        """ Separate the row number from the entity in the result set
            Keep a note of the first and last row index

        :param rows: iterable of tuples of the entity and a row number
        :yields: mapped business object instances
        """
        self.start_index = None
        self.end_index = None

        for instance, row_number in rows:
            row_index = row_number - 1
            if self.start_index is None:
                self.start_index = row_index
            self.end_index = row_index
            yield instance

    def collection(self):
        query = self._prepare_query()
        instance_generator = self._peel_off_row_number(query.all())
        return self._model_collection(instance_generator)

    def delete(self):
        query = self._prepare_query()
        query.delete()

    def __len__(self):
        query = self._prepare_query()
        return query.count()

    def __iter__(self):
        return iter(self.collection())

    def instance_finder(self, lookup_fieldname, value_cast):

        # use list() to instantiate the collection rather than query each time
        collection = self._model_collection(list(self.collection()))

        def lookup_instance(value, _):
            if not value:
                return None
            else:
                correct_type_value = value_cast(value) if value_cast else value
                instances = collection.lookup(correct_type_value, lookup_fieldname)
                return next(instances)

        return lookup_instance
