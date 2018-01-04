__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.io.gsheet_integration import get_gsheet_fields, load_class
from a_tuin.metadata import StringField, Mapping

from glod.db.fund import FundRestriction, Fund
from glod.db.account import AccountQuery


FUND_RESTRICTION_MAP = {
    '01. unrestricted': FundRestriction.Unrestricted,
    '02. restricted': FundRestriction.Restricted,
    '03. endowment': FundRestriction.Endowment,
}


def conform_fund_restriction(value, _):
    return FUND_RESTRICTION_MAP.get(value.lower(), FundRestriction.Unrestricted)


def conform_yes_no(value, _):
    return value.lower() == 'yes'


def funds_from_gsheet(session, extract_from_detailed_ledger):

    fund_gsheet = get_gsheet_fields(
        Fund,
        {
            'name': 'fund',
            'restriction': 'type',
            'is parish fund': 'parish fund',
            'account': 'bank account id'
        }
    )
    fund_gsheet['restriction'] = StringField('restriction')
    fund_gsheet['parish fund'] = StringField('parish fund')
    fund_gsheet['bank account id'] = StringField('bank account id')
    field_casts = {
        'type': conform_fund_restriction,
        'parish fund': conform_yes_no,
        'bank account id': AccountQuery(session).instance_finder('reference_no', int)
    }
    fund_mapping = Mapping(fund_gsheet, Fund.constructor_parameters, field_casts=field_casts)
    funds = extract_from_detailed_ledger(
        'funds',
        'A11',
        ('fund', 'type', 'parish fund', 'bank account id')
    )
    load_class(session, funds, fund_mapping, Fund)
