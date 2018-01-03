__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""


from sqlalchemy import (
    Enum,
)

from a_tuin.db.mapper import DB_COLUMN_TYPE_MAP

from glod.model.account import AccountStatusField, AccountStatus
from glod.model.fund import FundTypeField, FundType
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
    OrganisationType,
    OrganisationTypeField
)
from glod.model.person import PersonStatus, PersonStatusField
from glod.model.organisation_address import OrganisationAddressStatus, OrganisationAddressStatusField
from glod.model.counterparty import StandingOrderDonorField, StandingOrderDonor
from glod.model.transaction import (
    PaymentMethod,
    PaymentMethodField,
    IncomeExpenditure,
    IncomeExpenditureField,
)

DB_COLUMN_TYPE_MAP[AccountStatusField] = Enum(AccountStatus)

DB_COLUMN_TYPE_MAP[FundTypeField] = Enum(FundType)

DB_COLUMN_TYPE_MAP[NominalAccountSOFAHeadingField] = Enum(NominalAccountSOFAHeading)
DB_COLUMN_TYPE_MAP[NominalAccountCategoryField] = Enum(NominalAccountCategory)
DB_COLUMN_TYPE_MAP[NominalAccountSubCategoryField] = Enum(NominalAccountSubCategory)

DB_COLUMN_TYPE_MAP[OrganisationStatusField] = Enum(OrganisationStatus)
DB_COLUMN_TYPE_MAP[OrganisationTypeField] = Enum(OrganisationType)

DB_COLUMN_TYPE_MAP[OrganisationAddressStatusField] = Enum(OrganisationAddressStatus)

DB_COLUMN_TYPE_MAP[PersonStatusField] = Enum(PersonStatus)

DB_COLUMN_TYPE_MAP[StandingOrderDonorField] = Enum(StandingOrderDonor)

DB_COLUMN_TYPE_MAP[PaymentMethodField] = Enum(PaymentMethod)
DB_COLUMN_TYPE_MAP[IncomeExpenditureField] = Enum(IncomeExpenditure)
