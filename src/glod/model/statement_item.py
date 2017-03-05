__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

from glod.metadata import (
    ObjectReferenceField,
    StringField,
    DateField,
    DecimalField,
    ArgsFieldGroup,
    ObjectFieldGroupMixin
)


class StatementItem(ObjectFieldGroupMixin):

    constructor = ArgsFieldGroup(
        (
            ObjectReferenceField('account'),
            DateField('date', strfmt='%d/%m/%Y'),
            StringField('details'),
            StringField('currency'),
            DecimalField('debit'),
            DecimalField('credit'),
            DecimalField('balance'),
        )
    )

    def __init__(self, *args, **kwargs):
        constructor_to_internal = self.map_constructor_to_internal(self.constructor)

        constructor_to_internal.update_in_place((args, kwargs), self)

        self._detail_override = None
        self._designated_balance = None
