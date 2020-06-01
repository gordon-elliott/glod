__copyright__ = 'Copyright(c) Gordon Elliott 2020'

""" 
"""

from enum import IntEnum

from a_tuin.metadata import (
    ObjectFieldGroupBase, Collection, IntEnumField, DecimalField,
    IntField, DateField, DescriptionField, StringField
)


class SubmissionStatus(IntEnum):
    Preparing = 1
    Posted = 2
    Revoked = 3


class SubmissionStatusField(IntEnumField):
    def __init__(self, name, is_mutable=True, required=False, default=None, description=None, validation=None):
        super().__init__(name, SubmissionStatus, is_mutable, required, default, description, validation)


class TaxRebateSubmission(ObjectFieldGroupBase):
    # Data usage
    #
    # Record of the years in which a person's PPS was submitted in a rebate claim

    public_interface = (
        SubmissionStatusField(
            'status',
            required=True,
            default=SubmissionStatus.Preparing,
            description='Records what stage in its lifecycle the submission is at.'
        ),
        IntField('FY', required=True),
        DecimalField('calculated_rebate'),
        DateField('filing_date'),
        DecimalField('estimated_rebate', description='Estimated rebate from CDS1 form.'),
        StringField('notice_number'),
        DescriptionField('notes'),
    )


class TaxRebateSubmissionCollection(Collection):
    pass
