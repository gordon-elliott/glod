__copyright__ = 'Copyright(c) Gordon Elliott 2020'

""" 
"""

from a_tuin.metadata import (
    ObjectFieldGroupBase,
    ObjectReferenceField,
    Collection,
)


class PersonRebateSubmission(ObjectFieldGroupBase):

    public_interface = (
        ObjectReferenceField('person'),
        ObjectReferenceField('tax_rebate_submission'),
    )


class PersonRebateSubmissionCollection(Collection):
    pass
