__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

from glod.metadata import ObjectReferenceField, StringField, DateField, DictFieldGroup, ObjectFieldGroupMixin


class StatementItem(ObjectFieldGroupMixin):

    constructor = DictFieldGroup(
        (
            ObjectReferenceField('account'),
            DateField('date', strfmt='%d/%m/%Y'),
            StringField('details'),
            StringField('currency'),
            StringField('debit'),
            StringField('credit'),
            StringField('balance'),
        )
    )

    def __init__(self, **kwargs):
        constructor_to_internal = self.map_constructor_to_internal(self.constructor)

        constructor_to_internal.update_in_place(kwargs, self)

        self._detail_override = None
        self._designated_balance = None
