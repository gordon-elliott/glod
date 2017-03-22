__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""


class Collection(object):
    def __init__(self, items):
        self._items = items

    def lookup(self, id_to_match, field):
        for item in self._items:
            if getattr(item, field) == id_to_match:
                yield item

    def __len__(self):
        return len(self._items)