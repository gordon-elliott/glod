__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from a_tuin.db import RelationMap, TableMap, PagedQuery, InstanceQuery

from glod.model.tax_rebate import TaxRebate, TaxRebateCollection
from glod.model.references import tax_rebate__person

from glod.db.db_column_type_map import DB_COLUMN_TYPE_MAP
from glod.db.constants import SCHEMA_NAME


TableMap(TaxRebate, SCHEMA_NAME, 'tax_rebate', DB_COLUMN_TYPE_MAP, RelationMap(
    tax_rebate__person,
    'person._id',
    backref='tax_rebates',
    lazy='joined'
))


class TaxRebateInstanceQuery(InstanceQuery):
    def __init__(self, session):
        super().__init__(TaxRebate, TaxRebateCollection, session)


class TaxRebateQuery(PagedQuery):
    def __init__(self, session):
        super().__init__(TaxRebate, TaxRebateCollection, session)
