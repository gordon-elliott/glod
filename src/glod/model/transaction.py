__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

# id	reference	year	month	day	counterparty name	payment method	description	amount	subject	income/expenditure	FY	fund

from enum import IntEnum

from a_tuin.metadata import (
    ObjectFieldGroupBase,
    IntField,
    IntEnumField,
    StringField,
    DescriptionField,
    DecimalField,
    ObjectReferenceField,
    Collection,
)


class PaymentMethod(IntEnum):
    BankCharges = 1
    BankTax = 2
    BillpayOnline = 3
    CashLodgmentEnvelopes = 4
    CashLodgmentOther = 5
    CashLodgmentPlate = 6
    Cheque = 7
    DirectDebit = 8
    DirectPayment = 9
    DirectTransfer = 10
    InBranch = 11
    StandingOrderMonthly = 12
    StandingOrderOther = 13
    StandingOrderQuarterly = 14
    StandingOrders = 15
    UnrealisedGainLoss = 16


class PaymentMethodField(IntEnumField):
    def __init__(self, name, is_mutable=True, required=False, default=None, description=None, validation=None, use_custom_properties=False):
        super().__init__(name, PaymentMethod, is_mutable, required, default, description, validation, use_custom_properties)


class IncomeExpenditure(IntEnum):
    Income = 1
    Expenditure = 2


class IncomeExpenditureField(IntEnumField):
    def __init__(self, name, is_mutable=True, required=False, default=None, description=None, validation=None, use_custom_properties=False):
        super().__init__(name, IncomeExpenditure, is_mutable, required, default, description, validation, use_custom_properties)


class Transaction(ObjectFieldGroupBase):

    public_interface = (
        IntField('reference_no'),
        StringField('public_code'),
        IntField('year'),
        IntField('month'),
        IntField('day'),
        ObjectReferenceField('counterparty'),
        PaymentMethodField('payment_method'),
        DescriptionField('description'),
        DecimalField('amount'),
        ObjectReferenceField('subject'),
        IncomeExpenditureField('income_expenditure'),
        StringField('FY'),
        ObjectReferenceField('fund'),
    )


class TransactionCollection(Collection):
    pass
