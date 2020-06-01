__copyright__ = "Copyright (c) Gordon Elliott 2020"


from a_tuin.db import TableMap, PagedQuery, InstanceQuery

from glod.model.tax_rebate_submission import TaxRebateSubmission, TaxRebateSubmissionCollection

from glod.db.db_column_type_map import DB_COLUMN_TYPE_MAP
from glod.db.constants import SCHEMA_NAME


TableMap(TaxRebateSubmission, SCHEMA_NAME, 'tax_rebate_submission', DB_COLUMN_TYPE_MAP)


class TaxRebateSubmissionInstanceQuery(InstanceQuery):
    def __init__(self, session):
        super().__init__(TaxRebateSubmission, TaxRebateSubmissionCollection, session)


class TaxRebateSubmissionQuery(PagedQuery):
    def __init__(self, session):
        super().__init__(TaxRebateSubmission, TaxRebateSubmissionCollection, session)
