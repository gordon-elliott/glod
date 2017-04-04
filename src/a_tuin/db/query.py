__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""


class Query(object):

    def __init__(self, model_class, model_collection, session):
        self._session = session
        self._model_class = model_class
        self._model_collection = model_collection

        self._query = self._session.query(self._model_class)

    def __iter__(self):
        return iter(self.collection())

    def collection(self):
        return self._model_collection(self._query.all())

    def __len__(self):
        return self._query.count()

    def offset(self, num_items):
        self._query = self._query.offset(num_items)
        return self

    def limit(self, num_items):
        self._query = self._query.limit(num_items)
        return self

    def filter(self, *criteria):
        self._query = self._query.filter(*criteria)
        return self

    def delete(self):
        self._query.delete()