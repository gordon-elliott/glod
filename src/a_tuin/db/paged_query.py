__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from sqlalchemy import func

from a_tuin.db.query import Query


ROW_NUMBER_COLUMN_NAME = '_row_number'


class PagedQuery(Query):
    """ Provide paging logic on a result set by including a row number
        with the entity columns. The row number starts at 1 so it needs
        to be adjusted to a zero-based index

    """

    def __init__(self, model_class, model_collection, session):
        super().__init__(model_class, model_collection, session)

        # include a row number column
        self.row_number_column = func.row_number().over().label(ROW_NUMBER_COLUMN_NAME)
        self._query = self._query.add_columns(self.row_number_column)

    def __iter__(self):
        return iter(self.collection())

    def _peel_off_row_number(self, rows):
        """ Separate the row number from the entity in the result set
            Keep a note of the first and last row number

        :param rows: iterable of tuples of the entity and a row number
        :yields: mapped business object instances
        """
        self.start_index = None
        self.end_index = None

        for instance, row_number in rows:
            if self.start_index is None:
                self.start_index = row_number - 1
            self.end_index = row_number - 1
            yield instance

    def collection(self):
        instance_generator = self._peel_off_row_number(self._query.all())
        return self._model_collection(instance_generator)

    def __len__(self):
        return self._query.count()

    def offset(self, offset):
        self._query = self._query.from_self().filter(self.row_number_column > offset + 1)
        return self

    def limit(self, num_items):
        self._query = self._query.limit(num_items)
        return self

    def criteria_from_dict(self, filters):
        columns_collection = self._model_class.c
        for filter_field, filter_value in filters.items():
            column = columns_collection.get(filter_field)
            if column is not None:
                yield column.__eq__(filter_value)
                # TODO allow custom operators

    def filter(self, *criteria):
        self._query = self._query.filter(*criteria)
        return self

    def delete(self):
        self._query.delete()
