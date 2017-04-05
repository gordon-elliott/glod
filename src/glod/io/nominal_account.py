__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.io.gsheet_integration import get_gsheet_fields, load_class
from a_tuin.metadata import (
    Mapping,
    StringField,
    replace_underscore_with_space
)

from glod.db.nominal_account import (
    NominalAccount,
    NominalAccountCollection,
    NominalAccountSOFAHeading,
    NominalAccountCategory,
    NominalAccountSubCategory,
)


SOFA_HEADING_MAP = {
    'Donations and legacies': NominalAccountSOFAHeading.Donations_and_legacies,
    'Income from charitable activities': NominalAccountSOFAHeading.Income_from_charitable_activities,
    'Other trading activities': NominalAccountSOFAHeading.Other_trading_activities,
    'Investments': NominalAccountSOFAHeading.Investments,
    'Other income': NominalAccountSOFAHeading.Other_income,
    'Raising funds': NominalAccountSOFAHeading.Raising_funds,
    'Expenditure on charitable activities': NominalAccountSOFAHeading.Expenditure_on_charitable_activities,
    'Other expenditure': NominalAccountSOFAHeading.Other_expenditure,
}


class SOFAHeadingString(StringField):
    def conform_value(self, value):
        return SOFA_HEADING_MAP.get(value)


NOMINAL_ACCOUNT_CATEGORY_MAP = {
    'Income': NominalAccountCategory.Income,
    'Expenditure': NominalAccountCategory.Expenditure,
    'Fixed assets': NominalAccountCategory.Fixed_assets,
    'Current assets': NominalAccountCategory.Current_assets,
    'Liabilities': NominalAccountCategory.Liabilities,
}


class NominalAccountCategoryString(StringField):
    def conform_value(self, value):
        return NOMINAL_ACCOUNT_CATEGORY_MAP[value]


NOMINAL_ACCOUNT_SUB_CATEGORY_MAP = {
    'Tangible assets': NominalAccountSubCategory.Tangible_assets,
    'Investments': NominalAccountSubCategory.Investments,
    'Debtors': NominalAccountSubCategory.Debtors,
    'Cash at bank and in hand': NominalAccountSubCategory.Cash_at_bank_and_in_hand,
    'Creditors: Amounts falling due in one year': NominalAccountSubCategory.Creditors_Amounts_falling_due_in_one_year,
    'Creditors: Amounts falling due after more than one year': NominalAccountSubCategory.Creditors_Amounts_falling_due_after_more_than_one_year,
    'Agency accounts': NominalAccountSubCategory.Agency_accounts,
    'Reserves': NominalAccountSubCategory.Reserves,
}


class NominalAccountSubCategoryString(StringField):
    def conform_value(self, value):
        return NOMINAL_ACCOUNT_SUB_CATEGORY_MAP.get(value)


def nominal_accounts_from_gsheet(session, extract_from_detailed_ledger):
    nominal_account_gsheet = get_gsheet_fields(
        NominalAccount,
        {
            'code': 'Code',
            'description': 'Description',
            'SOFA heading': 'SOFA heading',
            'category': 'Category',
            'sub category': 'Sub-category',
        }
    )
    nominal_account_gsheet['SOFA heading'] = SOFAHeadingString('SOFA heading')
    nominal_account_gsheet['Category'] = NominalAccountCategoryString('Category')
    nominal_account_gsheet['Sub-category'] = NominalAccountSubCategoryString('Sub-category')
    nominal_account_mapping = Mapping(nominal_account_gsheet, NominalAccount.constructor_parameters)
    nominal_accounts = extract_from_detailed_ledger(
        'RCB Nominal Accounts',
        'A1',
        ('Code', 'Description', 'SOFA heading', 'Category', 'Sub-category')
    )
    load_class(session, nominal_accounts, nominal_account_mapping, NominalAccount)