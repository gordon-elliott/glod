__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""


from sqlalchemy import (
    Enum,
)

from a_tuin.db.mapper import DB_COLUMN_TYPE_MAP

from glod.model.account import AccountStatusField, AccountStatus
from glod.model.fund import FundRestrictionField, FundRestriction
from glod.model.nominal_account import (
    NominalAccountSOFAHeadingField,
    NominalAccountSOFAHeading,
    NominalAccountCategoryField,
    NominalAccountCategory,
    NominalAccountSubCategoryField,
    NominalAccountSubCategory,
)
from glod.model.organisation import (
    OrganisationStatus,
    OrganisationStatusField,
    OrganisationCategory,
    OrganisationCategoryField
)
from glod.model.person import PersonStatus, PersonStatusField
from glod.model.organisation_address import OrganisationAddressStatus, OrganisationAddressStatusField
from glod.model.pps import PPSStatus, PPSStatusField
from glod.model.tax_rebate_submission import SubmissionStatus, SubmissionStatusField
from glod.model.statement_item import StatementItemDesignatedBalance, StatementItemDesignatedBalanceField
from glod.model.transaction import (
    PaymentMethod,
    PaymentMethodField,
    IncomeExpenditure,
    IncomeExpenditureField,
)

DB_COLUMN_TYPE_MAP[AccountStatusField] = Enum(AccountStatus, inherit_schema=True)

DB_COLUMN_TYPE_MAP[FundRestrictionField] = Enum(FundRestriction, inherit_schema=True)

DB_COLUMN_TYPE_MAP[NominalAccountSOFAHeadingField] = Enum(NominalAccountSOFAHeading, inherit_schema=True)
DB_COLUMN_TYPE_MAP[NominalAccountCategoryField] = Enum(NominalAccountCategory, inherit_schema=True)
DB_COLUMN_TYPE_MAP[NominalAccountSubCategoryField] = Enum(NominalAccountSubCategory, inherit_schema=True)

DB_COLUMN_TYPE_MAP[OrganisationStatusField] = Enum(OrganisationStatus, inherit_schema=True)
DB_COLUMN_TYPE_MAP[OrganisationCategoryField] = Enum(OrganisationCategory, inherit_schema=True)

DB_COLUMN_TYPE_MAP[OrganisationAddressStatusField] = Enum(OrganisationAddressStatus, inherit_schema=True)

DB_COLUMN_TYPE_MAP[PersonStatusField] = Enum(PersonStatus, inherit_schema=True)

DB_COLUMN_TYPE_MAP[PPSStatusField] = Enum(PPSStatus, inherit_schema=True)

DB_COLUMN_TYPE_MAP[SubmissionStatusField] = Enum(SubmissionStatus, inherit_schema=True)

DB_COLUMN_TYPE_MAP[StatementItemDesignatedBalanceField] = Enum(StatementItemDesignatedBalance, inherit_schema=True)

DB_COLUMN_TYPE_MAP[PaymentMethodField] = Enum(PaymentMethod, inherit_schema=True)
DB_COLUMN_TYPE_MAP[IncomeExpenditureField] = Enum(IncomeExpenditure, inherit_schema=True)
