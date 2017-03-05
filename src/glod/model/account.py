__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

from glod.metadata import StringField, IntField, ArgsFieldGroup, ObjectFieldGroupMixin


class Account(ObjectFieldGroupMixin):

    constructor = ArgsFieldGroup(
        (
            IntField('id'),
            StringField('purpose'),
            StringField('status'),
            StringField('name'),
            StringField('institution'),
            StringField('sort_code'),
            StringField('account_no'),
            StringField('BIC'),
            StringField('IBAN'),
        )
    )

    def __init__(self, *args, **kwargs):
        constructor_to_internal = self.map_constructor_to_internal(self.constructor)

        constructor_to_internal.update_in_place((args, kwargs), self)
