__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" Facade for a collection of model instances
"""

import logging

from functools import wraps


LOG = logging.getLogger(__name__)


def chainable(generator_method):
    """ Decorator for use with Collection class
        Allows for chained invocation of filter methods and deferred iteration

    :param generator_method callable: generator method to decorate; must consume the iterable
        passed in the second parameter
    :return: wrapped generator method
    """

    @wraps(generator_method)
    def wrapped_generator(self, *method_args, **method_kwargs):
        # reset flag that indicates that all the items have been processed by the generators
        self._filter_applied = False
        # self._filtered updated with the new generator
        self._filtered = generator_method(self, self._filtered, *method_args, **method_kwargs)
        # returning self - the Collection - allows the calls to be chained
        return self

    return wrapped_generator


class Collection(object):
    """ Collection of model instances

        Encapsulate implementation of collection operations. In particular, calling code
        need not know when the underlying instances are processed. For efficient use of memory
        it is often desirable to defer instantiating a collection until the latest possible point.
    """

    def __init__(self, items):
        self._items = items
        self._items_iter = None
        self._filtered = iter(items)
        self._filter_applied = True

    def __iter__(self):
        if self._filter_applied:
            self._items_iter = iter(self._items)
        else:
            self._items = []
        return self

    def __next__(self):
        try:
            items = self._items_iter if self._filter_applied else self._filtered
            item = next(items)
            if not self._filter_applied:
                self._items.append(item)
            return item
        except StopIteration:
            self._filter_applied = True
            raise

    def lookup(self, id_to_match, fieldname):
        for item in self:
            if getattr(item, fieldname) == id_to_match:
                yield item

    def lookup_map(self, fieldname):
        lookup_dict = {}
        duplicates = set()
        for item in self:
            key = getattr(item, fieldname)
            if key is not None:
                if key in lookup_dict:
                    # remove ambiguous key and first mapping
                    del lookup_dict[key]
                    duplicates.add(key)
                else:
                    lookup_dict[key] = item

        if duplicates:
            LOG.warning('Duplicates excluded from {} lookup map {}'.format(fieldname, duplicates))

        return lookup_dict

    @chainable
    def not_null(self, items, fieldname):
        for item in items:
            if getattr(item, fieldname) is not None:
                yield item

    @chainable
    def is_null(self, items, fieldname):
        for item in items:
            if getattr(item, fieldname) is None:
                yield item

    @chainable
    def is_empty(self, items, fieldname):
        for item in items:
            if len(getattr(item, fieldname)) == 0:
                yield item

    @chainable
    def filter(self, items, item_expression):
        for item in items:
            if item_expression(item):
                yield item
