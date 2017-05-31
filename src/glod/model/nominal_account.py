__copyright__ = 'Copyright(c) Gordon Elliott 2017'

"""
"""

from enum import IntEnum

from a_tuin.metadata import IntEnumField, StringField, ObjectFieldGroupBase, Collection


class NominalAccountSOFAHeading(IntEnum):
    Donations_and_legacies = 1
    Income_from_charitable_activities = 2
    Other_trading_activities = 3
    Investments = 4
    Other_income = 5
    Raising_funds = 6
    Expenditure_on_charitable_activities = 7
    Other_expenditure = 8


class NominalAccountSOFAHeadingField(IntEnumField):
    def __init__(self, name, is_mutable=True, required=False, default=None, description=None, validation=None):
        super().__init__(name, NominalAccountSOFAHeading, is_mutable, required, default, description, validation)


class NominalAccountCategory(IntEnum):
    Income = 1
    Expenditure = 2
    Fixed_assets = 3
    Current_assets = 4
    Liabilities = 5

class NominalAccountCategoryField(IntEnumField):
    def __init__(self, name, is_mutable=True, required=False, default=None, description=None, validation=None):
        super().__init__(name, NominalAccountCategory, is_mutable, required, default, description, validation)


class NominalAccountSubCategory(IntEnum):
    Tangible_assets = 1
    Investments = 2
    Debtors = 3
    Cash_at_bank_and_in_hand = 4
    Creditors_Amounts_falling_due_in_one_year = 5
    Creditors_Amounts_falling_due_after_more_than_one_year = 6
    Agency_accounts = 7
    Reserves = 8


class NominalAccountSubCategoryField(IntEnumField):
    def __init__(self, name, is_mutable=True, required=False, default=None, description=None, validation=None):
        super().__init__(name, NominalAccountSubCategory, is_mutable, required, default, description, validation)


class NominalAccount(ObjectFieldGroupBase):

    public_interface = (
        StringField('code', is_mutable=False),
        StringField('description'),
        NominalAccountSOFAHeadingField('SOFA_heading'),
        NominalAccountCategoryField('category'),
        NominalAccountSubCategoryField('sub_category'),
    )


class NominalAccountCollection(Collection):
    pass
