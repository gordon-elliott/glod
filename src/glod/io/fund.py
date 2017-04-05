__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.io.gsheet_integration import get_gsheet_fields, load_class
from a_tuin.metadata import StringField, Mapping

from glod.db.fund import FundType, Fund
from glod.db.account import AccountQuery


FUND_TYPE_MAP = {
    '01. unrestricted': FundType.Unrestricted,
    '02. restricted': FundType.Restricted,
    '03. endowment': FundType.Endowment,
}


class FundTypeString(StringField):
    def conform_value(self, value):
        return FUND_TYPE_MAP.get(value.lower(), FundType.Unrestricted)


class YesNoString(StringField):
    def conform_value(self, value):
        return value.lower() == 'yes'


def funds_from_gsheet(session, extract_from_detailed_ledger):
    account_collection = AccountQuery(session).collection()

    class AccountStringField(StringField):
        def conform_value(self, value):
            if not value:
                return None
            else:
                accounts = account_collection.lookup(int(value), '_reference_no')
                return next(accounts)

    fund_gsheet = get_gsheet_fields(
        Fund,
        {'name': 'fund', 'is parish fund': 'parish fund', 'account': 'bank account id'}
    )
    fund_gsheet['type'] = FundTypeString('type')
    fund_gsheet['parish fund'] = YesNoString('parish fund')
    fund_gsheet['bank account id'] = AccountStringField('bank account id')
    fund_mapping = Mapping(fund_gsheet, Fund.constructor_parameters)
    funds = extract_from_detailed_ledger(
        'funds',
        'A11',
        ('fund', 'type', 'parish fund', 'bank account id')
    )
    load_class(session, funds, fund_mapping, Fund)