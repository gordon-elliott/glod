__copyright__ = 'Copyright(c) Gordon Elliott 2020'

from a_tuin.in_out.gsheet_integration import load_class
from a_tuin.metadata import Mapping, UnusedField, ListFieldGroup, IntField, StringField
from glod.in_out.casts import strip_commas, cast_dmy_date_from_string
from glod.model.tax_rebate_submission import SubmissionStatus
from glod.model.tax_rebate_submission import TaxRebateSubmission


def tax_rebate_submissions_from_gsheet(session, extract_from_tax_rebates):

    gs_field_status = StringField('status')
    gs_field_year = IntField('year')
    gs_field_cal_rebate = StringField('calculated rebate')
    gs_field_filing_date = StringField('filing date')
    gs_field_est_rebate = StringField('estimated rebate from CDS1')
    gs_field_notice_no = StringField('notice number')
    gs_field_notes = StringField('notes')
    
    tax_rebates_gsheet = ListFieldGroup(
        (
            gs_field_status,
            gs_field_year,
            UnusedField('parishoner count'),
            UnusedField('donor count'),
            UnusedField('donations'),
            gs_field_cal_rebate,
            gs_field_filing_date,
            gs_field_est_rebate,
            gs_field_notice_no,
            gs_field_notes
        )
    )

    field_mappings = tuple(zip(
        (
            gs_field_status,
            gs_field_year,
            gs_field_cal_rebate,
            gs_field_filing_date,
            gs_field_est_rebate,
            gs_field_notice_no,
            gs_field_notes
        ),
        TaxRebateSubmission.constructor_parameters
    ))

    field_casts = {
        'status': lambda v, _: SubmissionStatus.Posted if v == 'posted' else SubmissionStatus.Revoked,
        'calculated rebate': strip_commas,
        'filing date': cast_dmy_date_from_string,
        'estimated rebate from CDS1': strip_commas
    }
    tax_rebates_mapping = Mapping(tax_rebates_gsheet, TaxRebateSubmission.constructor_parameters, field_mappings, field_casts)
    tax_rebate_submissions = extract_from_tax_rebates(
        'records',
        'B1',
        (
            'status', 'year', 'parishoner count', 'donor count', 'donations',
            'calculated rebate', 'filing date', 'estimated rebate from CDS1', 'notice number',
            'notes'
        )
    )
    load_class(session, tax_rebate_submissions, tax_rebates_mapping, TaxRebateSubmission)
