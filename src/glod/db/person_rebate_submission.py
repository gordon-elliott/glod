__copyright__ = "Copyright (c) Gordon Elliott 2020"


from a_tuin.db import TableMap, RelationMap, PagedQuery, InstanceQuery

from glod.model.person_rebate_submission import PersonRebateSubmission, PersonRebateSubmissionCollection
from glod.model.references import person_rebate_submission__person, person_rebate_submission__tax_rebate_submission

from glod.db.db_column_type_map import DB_COLUMN_TYPE_MAP
from glod.db.constants import SCHEMA_NAME


TableMap(
    PersonRebateSubmission,
    SCHEMA_NAME,
    'person_rebate_submission',
    DB_COLUMN_TYPE_MAP,
    RelationMap(
        person_rebate_submission__tax_rebate_submission,
        'tax_rebate_submission._id',
        backref='people',
        lazy='joined'
    ), RelationMap(
        person_rebate_submission__person,
        'person._id',
        backref='tax_rebate_submissions',
        lazy='joined'
    )
)


class PersonRebateSubmissionInstanceQuery(InstanceQuery):
    def __init__(self, session):
        super().__init__(PersonRebateSubmission, PersonRebateSubmissionCollection, session)


class PersonRebateSubmissionQuery(PagedQuery):
    def __init__(self, session):
        super().__init__(PersonRebateSubmission, PersonRebateSubmissionCollection, session)
