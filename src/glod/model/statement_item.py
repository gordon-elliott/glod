__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

from decimal import Decimal

from glod.metadata import (
    ObjectReferenceField,
    StringField,
    DateField,
    DecimalField,
    ArgsFieldGroup,
    ObjectFieldGroupMeta
)


class StatementItem(object, metaclass=ObjectFieldGroupMeta):

    constructor_parameters = ArgsFieldGroup(
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

    # metaclass takes care of dealing with the args
    def __init__(self, *args, **kwargs):
        self._detail_override = None
        self._designated_balance = None

    @property
    def debit(self):
        return self._debit if self._debit is not None else Decimal('0.00')

    @property
    def credit(self):
        return self._credit if self._credit is not None else Decimal('0.00')

    @property
    def net(self):
        return self.credit - self.debit
