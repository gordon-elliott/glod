__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

from decimal import Decimal

from a_tuin.metadata import (
    ObjectReferenceField,
    StringField,
    DateField,
    DecimalField,
    ObjectFieldGroupBase
)


class StatementItem(ObjectFieldGroupBase):

    public_interface = (
        (
            ObjectReferenceField('account'),
            DateField('date', strfmt='%d/%m/%Y', use_custom_properties=True),
            StringField('details'),
            StringField('currency'),
            DecimalField('debit', use_custom_properties=True),
            DecimalField('credit', use_custom_properties=True),
            DecimalField('balance'),
        )
    )

    # metaclass takes care of dealing with the args
    def __init__(self, *args, **kwargs):
        self._detail_override = None
        self._designated_balance = None

    @property
    def book_date(self):
        return self._date

    @book_date.setter
    def book_date(self, value):
        self._date = value

    @property
    def debit(self):
        return self._debit if self._debit is not None else Decimal('0.00')

    @debit.setter
    def debit(self, value):
        self._debit = value

    @property
    def credit(self):
        return self._credit if self._credit is not None else Decimal('0.00')

    @credit.setter
    def credit(self, value):
        self._credit = value

    @property
    def net(self):
        return self.credit - self.debit

    @property
    def month(self):
        return self._date.month
