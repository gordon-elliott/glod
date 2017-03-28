__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

from decimal import Decimal

from a_tuin.metadata import (
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
    def account(self):
        return self._account

    @account.setter
    def account(self, value):
        self._account = value

    @property
    def book_date(self):
        return self._date

    @book_date.setter
    def book_date(self, value):
        self._date = value

    @property
    def details(self):
        return self._details

    @details.setter
    def details(self, value):
        self._details = value

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, value):
        self._currency = value

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
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        self._balance = value

    @property
    def net(self):
        return self.credit - self.debit

    @property
    def month(self):
        return self._date.month