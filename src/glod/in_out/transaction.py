__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.in_out.gsheet_integration import load_class
from a_tuin.metadata import StringField, Mapping, UnusedField, ListFieldGroup

from glod.db.transaction import PaymentMethod, IncomeExpenditure, Transaction
from glod.db.counterparty import CounterpartyQuery
from glod.db.subject import SubjectQuery
from glod.db.fund import FundQuery

from glod.in_out.casts import strip_commas


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

    gs_field_reference_no = StringField('id')
    gs_field_public_code = StringField('reference')
    gs_field_year = StringField('year')
    gs_field_month = StringField('month')
    gs_field_day = StringField('day')
    gs_field_counterparty = StringField('counterparty_id')
    gs_field_payment_method = StringField('payment_method')
    gs_field_description = StringField('description')
    gs_field_amount = StringField('amount')
    gs_field_subject = StringField('subject')
    gs_field_income_expenditure = StringField('income_expenditure')
    gs_field_FY = StringField('FY')
    gs_field_fund = StringField('fund')
    gs_field_comments = StringField('comments')

    transaction_gsheet = ListFieldGroup(
        (
            gs_field_reference_no,
            gs_field_fund,
            gs_field_public_code,
            UnusedField('bank account'),
            UnusedField('compositeId'),
            gs_field_year,
            gs_field_month,
            gs_field_day,
            gs_field_counterparty,
            UnusedField('counterparty name'),
            UnusedField('household_id'),
            gs_field_payment_method,
            gs_field_description,
            gs_field_amount,
            gs_field_subject,
            gs_field_income_expenditure,
            gs_field_FY,
            UnusedField('sign'),
            UnusedField('net'),
            UnusedField('from bank statement'),
            UnusedField('reconciles'),
            UnusedField('bank stmt year'),
            UnusedField('year reconciles?'),
            UnusedField('monthText'),
            UnusedField('quarter'),
            UnusedField('subjectSummary'),
            UnusedField('fund type'),
            gs_field_comments,
        )
    )
    field_casts = {
        'counterparty_id': CounterpartyQuery(session).instance_finder('reference_no', int),
        'payment_method': cast_payment_method,
        'amount': strip_commas,
        'subject': SubjectQuery(session).instance_finder('name', None),
        'income_expenditure': cast_income_expenditure,
        'fund': FundQuery(session).instance_finder('name', None),
    }
    field_mappings = tuple(zip(
        (
            gs_field_reference_no,
            gs_field_public_code,
            gs_field_year,
            gs_field_month,
            gs_field_day,
            gs_field_counterparty,
            gs_field_payment_method,
            gs_field_description,
            gs_field_amount,
            gs_field_subject,
            gs_field_income_expenditure,
            gs_field_FY,
            gs_field_fund,
            gs_field_comments,
        ),
        Transaction.constructor_parameters
    ))
    transaction_mapping = Mapping(transaction_gsheet, Transaction.constructor_parameters, field_mappings, field_casts)
    transactions = extract_from_detailed_ledger(
        'transactions',
        'A1',
        (
            'id',
            'fund',
            'reference',
            'bank account',
            'compositeId',
            'year',
            'month',
            'day',
            'counterparty_id',
            'counterparty_name',
            'household_id',
            'payment_method',
            'description',
            'amount',
            'subject',
            'income/expenditure',
            'FY',
            'sign',
            'net',
            'from bank statement',
            'reconciles',
            'bank stmt year',
            'year reconciles?',
            'monthText',
            'quarter',
            'subjectSummary',
            'fund type',
            'comments'
        )
    )
    load_class(session, transactions, transaction_mapping, Transaction)
