__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.io.gsheet_integration import get_gsheet_fields, load_class
from a_tuin.metadata import StringField, Mapping

from glod.db.transaction import PaymentMethod, IncomeExpenditure, Transaction
from glod.db.counterparty import CounterpartyQuery
from glod.db.subject import SubjectQuery
from glod.db.fund import FundQuery

from glod.io.casts import strip_commas


PAYMENT_METHOD_MAP = {
    'bank charges': PaymentMethod.BankCharges,
    'bank tax': PaymentMethod.BankTax,
    'billpay online': PaymentMethod.BillpayOnline,
    'cash lodgment - envelopes': PaymentMethod.CashLodgmentEnvelopes,
    'cash lodgment - other': PaymentMethod.CashLodgmentOther,
    'cash lodgment - plate': PaymentMethod.CashLodgmentPlate,
    'cheque': PaymentMethod.Cheque,
    'direct debit': PaymentMethod.DirectDebit,
    'direct payment': PaymentMethod.DirectPayment,
    'direct transfer': PaymentMethod.DirectTransfer,
    'in branch': PaymentMethod.InBranch,
    'standing order - monthly': PaymentMethod.StandingOrderMonthly,
    'standing order - other': PaymentMethod.StandingOrderOther,
    'standing order - quarterly': PaymentMethod.StandingOrderQuarterly,
    'standing orders': PaymentMethod.StandingOrders,
    'unrealised gain/loss': PaymentMethod.UnrealisedGainLoss,
}


def cast_payment_method(value, _):
    return PAYMENT_METHOD_MAP.get(value.lower())


INCOME_EXPENDITURE_MAP = {
    'income': IncomeExpenditure.Income,
    'expenditure': IncomeExpenditure.Expenditure,
}


def cast_income_expenditure(value, _):
    return INCOME_EXPENDITURE_MAP[value]


def cast_lower(value):
    return value.lower()


def transactions_from_gsheet(session, extract_from_detailed_ledger):

    transaction_gsheet = get_gsheet_fields(
        Transaction,
        {
            'reference no': 'id',
            'public code': 'reference',
            'counterparty': 'counterparty name',
            'income expenditure': 'income/expenditure'
        }
    )
    transaction_gsheet['counterparty name'] = StringField('counterparty name')
    transaction_gsheet['payment method'] = StringField('payment method')
    transaction_gsheet['subject'] = StringField('subject')
    transaction_gsheet['income/expenditure'] = StringField('income/expenditure')
    transaction_gsheet['fund'] = StringField('fund')
    field_casts = {
        'counterparty name': CounterpartyQuery(session).instance_finder('lookup_name', cast_lower),
        'payment method': cast_payment_method,
        'amount': strip_commas,
        'subject': SubjectQuery(session).instance_finder('name', None),
        'income/expenditure': cast_income_expenditure,
        'fund': FundQuery(session).instance_finder('name', None),
    }
    transaction_mapping = Mapping(transaction_gsheet, Transaction.constructor_parameters, field_casts=field_casts)
    transactions = extract_from_detailed_ledger(
        'transactions',
        'A1',
        (
            'id',
            'reference',
            'year',
            'month',
            'day',
            'counterparty name',
            'payment method',
            'description',
            'amount',
            'subject',
            'income/expenditure',
            'FY',
            'fund'
        )
    )
    load_class(session, transactions, transaction_mapping, Transaction)
