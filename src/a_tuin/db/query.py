__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""


class Query(object):
    def __init__(self, model_class, model_collection, session):
        self._session = session
        self._model_class = model_class
        self._model_collection = model_collection


class InstanceQuery(Query):

    def instance(self, id):
        query = self._session.query(self._model_class)
        return query.get(id)
