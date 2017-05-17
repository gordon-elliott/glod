__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.io.gsheet_integration import get_gsheet_fields, load_class
from a_tuin.metadata import StringField, Mapping

from glod.db.fund import FundType, Fund
from glod.db.account import AccountQuery, AccountCollection


FUND_TYPE_MAP = {
    '01. unrestricted': FundType.Unrestricted,
    '02. restricted': FundType.Restricted,
    '03. endowment': FundType.Endowment,
}


def conform_fund_type(value, _):
    return FUND_TYPE_MAP.get(value.lower(), FundType.Unrestricted)


def conform_yes_no(value, _):
    return value.lower() == 'yes'


def funds_from_gsheet(session, extract_from_detailed_ledger):
    account_collection = AccountCollection(list(AccountQuery(session).collection()))

    def conform_account(value, _):
        if not value:
            return None
        else:
            accounts = account_collection.lookup(int(value), '_reference_no')
            return next(accounts)

    fund_gsheet = get_gsheet_fields(
        Fund,
        {'name': 'fund', 'is parish fund': 'parish fund', 'account': 'bank account id'}
    )
    fund_gsheet['type'] = StringField('type')
    fund_gsheet['parish fund'] = StringField('parish fund')
    fund_gsheet['bank account id'] = StringField('bank account id')
    field_casts = {
        'type': conform_fund_type,
        'parish fund': conform_yes_no,
        'bank account id': conform_account
    }
    fund_mapping = Mapping(fund_gsheet, Fund.constructor_parameters, field_casts=field_casts)
    funds = extract_from_detailed_ledger(
        'funds',
        'A11',
        ('fund', 'type', 'parish fund', 'bank account id')
    )
    load_class(session, funds, fund_mapping, Fund)
