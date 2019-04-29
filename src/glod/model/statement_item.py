__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""
import re

from decimal import Decimal
from enum import IntEnum

from a_tuin.metadata import (
    ObjectReferenceField,
    StringField,
    DateField,
    DecimalField,
    ObjectFieldGroupBase,
    IntEnumField
)


class StatementItemDesignatedBalance(IntEnum):
    No = 1
    Opening = 2
    Closing = 3


class StatementItemDesignatedBalanceField(IntEnumField):

    def __init__(self, name, is_mutable=True, required=False, default=None, description=None, validation=None):
        super().__init__(name, StatementItemDesignatedBalance, is_mutable, required, default, description, validation)


TRUNCATE_ON = (
    ' IE1',
    ' GTS',
    ' CT0',
    ' RT0',
)
TRUNCATE_ON_PATTERN = r'^(.*)(({}).*)$'.format('|'.join(TRUNCATE_ON))


class StatementItem(ObjectFieldGroupBase):

    public_interface = (
        ObjectReferenceField('account'),
        # TODO: allow properties to be named differently to internal/db fields
        DateField('date'),
        StringField('details'),
        StringField('currency'),
        DecimalField('debit', use_custom_properties=True),
        DecimalField('credit', use_custom_properties=True),
        DecimalField('balance'),
        StringField('detail_override'),
        StatementItemDesignatedBalanceField('designated_balance', default=StatementItemDesignatedBalance.No)
    )

    # metaclass takes care of dealing with the args
    def __init__(self, *args, **kwargs):
        self._designated_balance = None

    def __str__(self):
        return '{0.__class__.__name__}({0._account}, {0._date}, {0.trimmed_details})'.format(self)

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
    def year(self):
        return self._date.year

    @property
    def month(self):
        return self._date.month

    @property
    def day(self):
        return self._date.day

    @property
    def unified_details(self):
        return self._detail_override if self._detail_override else self._details

    @property
    def public_code(self):
        details = self.unified_details
        # lodgments
        if details.startswith('LODGMENT'):
            return details.replace('LODGMENT', '').strip()
        # direct payments out and in
        elif details.startswith('D0') or details.startswith('E0'):
            return details[0:6]
        # cheque numbers
        elif re.search(r'^\d{6}$', details):
            return details
        else:
            return None

    @property
    def trimmed_details(self):
        """ Drop any text after the specified strings

        :return:
        """
        return re.sub(
            TRUNCATE_ON_PATTERN,
            '\g<1>',
            self.unified_details
        )

